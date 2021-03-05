import itertools
from dataclasses import dataclass
from typing import Optional

import pyomo.environ as pe

from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class _ConstraintMaker:

    sets: MILPSets
    pars: MILPParameters
    vars: MILPVariables

    def make_define_loan_paid_off_indicator(self) -> pe.Constraint:
        def rule(_, l, t):
            return (self.vars.get_balance(l, t)) >= (
                (self.pars.get_loan_upper_bound(l)) * (self.vars.get_is_unpaid(l, t))
            )

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.working_periods_as_set),
            rule=rule,
        )

    def make_allocate_minimum_payments(self) -> pe.Constraint:
        def rule(_, i, t):
            if self.pars.get_is_guaranteed_investment(i):
                return pe.Constraint.Skip
            if t >= max(self.sets.working_periods_as_set):
                return pe.Constraint.Skip


            allocation = self.vars.get_allocation(i, t)
            if self.pars.get_is_investment(i):
                return self.pars.get_minimum_monthly_payment(i, t) <= allocation

            final_payment_order = self.pars.get_final_decision_period_index()
            allocation_slack = self.pars.get_monthly_allowance(t) * (
                1 - self.vars.get_is_unpaid(i, min(t + 1, final_payment_order))
            )

            if self.pars.get_is_revolving_loan(i):
                # mmp = -self.vars.get_balance(l, t) * self.pars.get_average_interest_rate(l, t) # TODO: make faster
                mmp = -self.pars.get_starting_balance(
                    i
                ) * self.pars.get_average_interest_rate(i, t)
                return mmp <= allocation + allocation_slack
            else:  # is instalment loan
                return (
                    self.pars.get_minimum_monthly_payment(i, t)
                    <= allocation + allocation_slack
                )

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.all_decision_periods_as_set),
            rule=rule,
        )

    def make_define_account_balance(self) -> pe.Constraint:
        def rule(_, i, t):
            cur_balance = self.vars.get_balance(i, t)

            if t == 0:
                starting_balance = self.pars.get_starting_balance(i)
                return cur_balance == starting_balance
            # elif t >= self.pars.get_instrument_final_payment_horizon(i).order:
            #     return self.vars.get_balance(i, t) == self.vars.get_balance(i, t - 1)
            elif self.pars.get_average_interest_rate(i, t - 1) == 0:
                prev_balance = self.vars.get_balance(i, t - 1)
                allocation = self.vars.get_allocation(i, t - 1)
                if self.pars.get_is_investment(i) or self.pars.get_is_guaranteed_investment(i):
                    withdrawal = self.vars.get_withdrawal(i, t)
                else:
                    withdrawal = 0
                n = self.sets.get_num_months_in_horizon(t)
                return cur_balance == prev_balance + (allocation - withdrawal) * n
            else:
                prev_balance = self.vars.get_balance(i, t - 1)
                r = 1 + self.pars.get_average_interest_rate(i, t - 1)
                n = self.sets.get_num_months_in_horizon(t)
                allocation = self.vars.get_allocation(i, t - 1)
                if self.pars.get_is_investment(i) or self.pars.get_is_guaranteed_investment(i):
                    withdrawal = self.vars.get_withdrawal(i, t)
                else:
                    withdrawal = 0
                return cur_balance == ((prev_balance * r ** n)
                    + (allocation - withdrawal) * (r ** n - 1) / (r - 1)
                )

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.all_decision_periods_as_set),
            rule=rule,
        )

    def make_total_payments_limit(self) -> pe.Constraint:
        def rule(_, t):
            return (
                sum(self.vars.get_allocation(i, t) for i in self.sets.instruments)
                + self.vars.get_allocation_slack(t)
                == self.pars.get_monthly_allowance(t)
            )

        return pe.Constraint(self.sets.all_decision_periods_as_set, rule=rule)

    def make_loans_are_non_positive(self) -> pe.Constraint:
        def rule(_, i, t):
            if self.pars.get_is_investment(i) or self.pars.get_is_guaranteed_investment(i):
                return self.vars.get_balance(i, t) >= 0
            else:
                return self.vars.get_balance(i, t) <= 0

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.all_decision_periods_as_set),
            rule=rule,
        )

    def make_pay_off_loans_by_end_date(self) -> pe.Constraint:
        def rule(_, l, t):
            if t < self.pars.get_instrument_final_payment_horizon(l).index - 1:
                return pe.Constraint.Skip
            else:
                return self.vars.get_loan_due_date_violation(
                    l, t
                ) >= -self.vars.get_balance(l, t)

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.working_periods_as_set),
            rule=rule,
        )

    def make_define_in_debt_indicator(self) -> pe.Constraint:
        def rule(_, t):
            count_of_unpaid_loans = sum(
                self.vars.get_is_unpaid(l, t) for l in self.sets.loans
            )
            total_loans = len(self.sets.loans)
            return self.vars.get_is_in_debt(t) >= count_of_unpaid_loans / total_loans

        if not self.pars.has_loans():
            return pe.Constraint.NoConstraint
        else:
            return pe.Constraint(
                itertools.product(self.sets.working_periods_as_set), rule=rule
            )

    def _get_allocation_volatility(self, t):
        return sum(
            self.vars.get_allocation(i, t) * self.pars.get_volatility(i)
            for i in self.sets.investments
        )

    def make_limit_total_risk(self) -> pe.Constraint:
        def rule(_, t):

            final_payment_order = self.pars.get_final_work_period_index()
            min_const_volatility = self.pars.get_min_investment_volatility()
            # fixed_volatility = self.pars.get_fixed_volatility(t)

            if self.pars.has_loans():
                min_volatility = min_const_volatility * (
                    1 - self.vars.get_is_in_debt(min(t + 1, final_payment_order))
                )
            else:
                min_volatility = min_const_volatility

            volatility_limit = (
                min_volatility
                + self.pars.get_user_risk_profile_as_fraction()
                * (self.pars.get_max_volatility() - min_volatility)
            )
            allocation_volatility = self._get_allocation_volatility(t)
            violation = self.vars.get_total_risk_violation(t)
            return (
                violation
                >= allocation_volatility
                - volatility_limit * self.pars.get_monthly_allowance(t)
            )

        if self.pars.has_investments() and self.pars.has_loans():
            return pe.Constraint(
                itertools.product(self.sets.working_periods_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint

    def make_limit_investment_risk(self) -> pe.Constraint:
        def rule(_, t):
            min_volatility = self.pars.get_min_investment_volatility()

            volatility_limit = (
                min_volatility
                + self.pars.get_user_risk_profile_as_fraction()
                * (self.pars.get_max_volatility() - min_volatility)
            )

            total_investment_allocations = sum(
                self.vars.get_allocation(i, t) for i in self.sets.investments
            )

            allocation_volatility = sum(
                self.vars.get_allocation(i, t) * self.pars.get_volatility(i)
                for i in self.sets.investments
            )

            violation = self.vars.get_investment_risk_violation(t)
            return (
                violation
                >= allocation_volatility
                - volatility_limit * total_investment_allocations
            )

        if self.pars.has_investments():
            return pe.Constraint(
                itertools.product(self.sets.working_periods_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint

    def make_define_taxable_income_in_bracket(self):
        def rule(_, t, e, b):
            pos = self.vars.get_pos_overflow_in_bracket(t, e, b)
            neg = self.vars.get_neg_overflow_in_bracket(t, e, b)
            rem = self.vars.get_remaining_marginal_income_in_bracket(t, e, b)
            # taxable_income = self.vars.get_taxable_monthly_income(t)
            taxable_income = self.pars.get_before_tax_monthly_income()
            bracket_cumulative_income = self.pars.get_bracket_cumulative_income(e, b)
            return pos - rem - neg == taxable_income - bracket_cumulative_income

        return pe.Constraint(
            itertools.product(self.sets.all_decision_periods_as_set, self.sets.taxing_entities_and_brackets),
            rule=rule
        )

    def make_limit_remaining_marginal_income_in_bracket(self):
        def rule(_, t, e, b):
            rem = self.vars.get_remaining_marginal_income_in_bracket(t, e, b)
            ub = self.pars.get_bracket_marginal_income(e, b)
            return rem <= ub

        return pe.Constraint(
            itertools.product(self.sets.all_decision_periods_as_set, self.sets.taxing_entities_and_brackets),
            rule=rule
        )

    def make_define_taxes_accrued_in_bracket(self):
        def rule(_, t, e, b):
            tax = self.vars.get_taxes_accrued_in_bracket(t, e, b)
            rem = self.vars.get_remaining_marginal_income_in_bracket(t, e, b)
            rate = self.pars.get_bracket_marginal_tax_rate(e, b)
            ub = self.pars.get_bracket_marginal_income(e, b)
            return tax == (ub - rem) * rate

        return pe.Constraint(
            itertools.product(self.sets.all_decision_periods_as_set, self.sets.taxing_entities_and_brackets),
            rule=rule
        )

    def make_satisfy_retirement_spending_requirement(self):
        def rule(_, t):
            all_withdrawals = sum(
                self.vars.get_withdrawal(i, t) for i in self.sets.investments_and_guaranteed_investments
            )
            spending = self.pars.get_minimum_monthly_retirement_spending(t)
            violation = self.vars.get_retirement_spending_violation(t)
            return violation >= spending - all_withdrawals
        if not self.sets.investments_and_guaranteed_investments:
            return pe.Constraint.NoConstraint
        else:
            return pe.Constraint(
                itertools.product(self.sets.retirement_periods_as_set),
                rule=rule
            )

    def make_zero_allocations_for_guaranteed_investments(self):
        def rule(_, i, t):
            if self.pars.get_is_guaranteed_investment(i):
                return self.vars.get_allocation(i, t) == 0
            else:
                return pe.Constraint.Skip

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.all_decision_periods_as_set),
            rule=rule
        )

@dataclass
class MILPConstraints:

    define_loan_paid_off_indicator: pe.Constraint
    allocate_minimum_payments: pe.Constraint
    define_account_balance: pe.Constraint
    total_payments_limit: pe.Constraint
    loans_are_non_positive: pe.Constraint
    pay_off_loans_by_end_date: pe.Constraint
    define_in_debt_indicator: pe.Constraint
    limit_total_risk: pe.Constraint
    limit_investment_risk: pe.Constraint
    define_taxable_income_in_bracket: pe.Constraint
    limit_remaining_marginal_income_in_bracket: pe.Constraint
    define_taxes_accrued_in_bracket: pe.Constraint
    satisfy_retirement_spending_requirement: pe.Constraint
    zero_allocations_for_guaranteed_investments: pe.Constraint

    @classmethod
    def create(
        cls, sets: MILPSets, pars: MILPParameters, vars_: MILPVariables
    ) -> "MILPConstraints":
        cm = _ConstraintMaker(sets=sets, pars=pars, vars=vars_)
        return MILPConstraints(
            define_loan_paid_off_indicator=cm.make_define_loan_paid_off_indicator(),
            allocate_minimum_payments=cm.make_allocate_minimum_payments(),
            define_account_balance=cm.make_define_account_balance(),
            total_payments_limit=cm.make_total_payments_limit(),
            loans_are_non_positive=cm.make_loans_are_non_positive(),
            pay_off_loans_by_end_date=cm.make_pay_off_loans_by_end_date(),
            define_in_debt_indicator=cm.make_define_in_debt_indicator(),
            limit_total_risk=cm.make_limit_total_risk(),
            limit_investment_risk=cm.make_limit_investment_risk(),
            define_taxable_income_in_bracket=cm.make_define_taxable_income_in_bracket(),
            limit_remaining_marginal_income_in_bracket=cm.make_limit_remaining_marginal_income_in_bracket(),
            define_taxes_accrued_in_bracket=cm.make_define_taxes_accrued_in_bracket(),
            satisfy_retirement_spending_requirement=cm.make_satisfy_retirement_spending_requirement(),
            zero_allocations_for_guaranteed_investments=cm.make_zero_allocations_for_guaranteed_investments()
        )
