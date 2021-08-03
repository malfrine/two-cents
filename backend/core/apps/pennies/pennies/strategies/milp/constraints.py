import itertools
from dataclasses import dataclass
from math import floor

import pyomo.environ as pe

from pennies.model.rrsp import RRSP_LIMIT_INCOME_FACTOR, RRIFMinPaymentCalculator
from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables
from pennies.utilities.datetime import MONTHS_IN_YEAR


@dataclass
class _ConstraintMaker:
    sets: MILPSets
    pars: MILPParameters
    vars: MILPVariables

    def get_post_tax_monthly_income(self, t):
        pre_tax_income = self.pars.get_before_tax_monthly_income(t)
        tax = sum(
            self.vars.get_taxes_accrued_in_bracket(t, e, b)
            for e, b in self.sets.taxing_entities_and_brackets
        )
        return pre_tax_income - tax

    def get_monthly_allowance(self, t):
        return self.pars.get_savings_fraction() * self.get_post_tax_monthly_income(t)

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

            allocation = self.vars.get_allocation(i, t)
            violation = self.vars.get_min_payment_violation(i, t)
            min_payment = self.pars.get_minimum_monthly_payment(i, t)
            if self.pars.get_is_investment(i):
                return violation >= min_payment - allocation

            final_payment_order = self.pars.get_final_work_period_index()
            big_m = (
                self.pars.get_before_tax_monthly_income(t)
                * self.pars.get_savings_fraction()
            )
            allocation_slack = big_m * (
                1 - self.vars.get_is_unpaid(i, min(t + 1, final_payment_order))
            )

            return violation >= min_payment - allocation - allocation_slack

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.working_periods_as_set),
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
                if self.pars.get_is_investment(
                    i
                ) or self.pars.get_is_guaranteed_investment(i):
                    withdrawal = self.vars.get_withdrawal(i, t - 1)
                else:
                    withdrawal = 0
                n = self.sets.get_num_months_in_decision_period(t)
                return cur_balance == prev_balance + (allocation - withdrawal) * n
            else:
                prev_balance = self.vars.get_balance(i, t - 1)
                r = 1 + self.pars.get_average_interest_rate(i, t - 1)
                n = self.sets.get_num_months_in_decision_period(t)
                allocation = self.vars.get_allocation(i, t - 1)
                if self.pars.get_is_investment(
                    i
                ) or self.pars.get_is_guaranteed_investment(i):
                    withdrawal = self.vars.get_withdrawal(i, t - 1)
                else:
                    withdrawal = 0
                return cur_balance == (
                    (prev_balance * r ** n)
                    + (allocation - withdrawal) * (r ** n - 1) / (r - 1)
                )

        return pe.Constraint(
            itertools.product(
                self.sets.instruments, self.sets.all_decision_periods_as_set
            ),
            rule=rule,
        )

    def make_total_payments_limit(self) -> pe.Constraint:
        def rule(_, t):
            return sum(
                self.vars.get_allocation(i, t) for i in self.sets.instruments
            ) == self.get_monthly_allowance(t)

        return pe.Constraint(self.sets.all_decision_periods_as_set, rule=rule)

    def make_loans_are_non_positive(self) -> pe.Constraint:
        def rule(_, i, t):
            if self.pars.get_is_investment(i) or self.pars.get_is_guaranteed_investment(
                i
            ):
                return self.vars.get_balance(i, t) >= 0
            else:
                return self.vars.get_balance(i, t) <= 0

        return pe.Constraint(
            itertools.product(
                self.sets.instruments, self.sets.all_decision_periods_as_set
            ),
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
            max_debt = -sum(self.pars.get_starting_balance(l) for l in self.sets.loans)
            current_debt = -sum(self.vars.get_balance(l, t) for l in self.sets.loans)
            return self.vars.get_is_in_debt(t) >= current_debt / max_debt

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

            if self.pars.has_loans():
                min_volatility = min_const_volatility * (
                    1 - self.vars.get_is_in_debt(min(t + 1, final_payment_order))
                )
            else:
                min_volatility = min_const_volatility

            volatility_limit = min_volatility + self.pars.get_user_risk_profile_as_fraction() * (
                self.pars.get_max_investment_volatility() - min_volatility
            )
            allocation_volatility = self._get_allocation_volatility(t)
            violation = self.vars.get_total_risk_violation(t)

            # allowance is not exact but it is needed to avoid quadratic solution
            allowance = (
                self.pars.get_before_tax_monthly_income(t)
                * self.pars.get_savings_fraction()
            )
            return violation >= allocation_volatility - volatility_limit * allowance

        if self.pars.has_investments() and self.pars.has_loans():
            return pe.Constraint(
                itertools.product(self.sets.working_periods_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint

    def make_limit_investment_risk(self) -> pe.Constraint:

        min_volatility = self.pars.get_min_investment_volatility()

        volatility_limit = min_volatility + self.pars.get_user_risk_profile_as_fraction() * (
            self.pars.get_max_investment_volatility() - min_volatility
        )

        def rule(_, t):

            total_investment_allocations = sum(
                self.vars.get_allocation(i, t) for i in self.sets.investments
            )

            allocation_volatility = sum(
                self.vars.get_allocation(i, t) * self.pars.get_volatility(i)
                for i in self.sets.investments
            )

            actual_volatility = allocation_volatility
            allowed_volatility = total_investment_allocations * volatility_limit

            violation = self.vars.get_investment_risk_violation(t)
            return violation >= actual_volatility - allowed_volatility

        if self.pars.has_investments():
            return pe.Constraint(
                itertools.product(self.sets.working_periods_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint

    def make_define_taxable_income_in_bracket(self):
        def rule(_, t, e, b):
            pos = self.vars.get_pos_overflow_in_bracket(t, e, b)
            rem = self.vars.get_remaining_marginal_income_in_bracket(t, e, b)
            taxable_income = self.vars.get_taxable_monthly_income(t)
            bracket_cumulative_income = self.pars.get_bracket_cumulative_income(e, b)
            return pos - rem == taxable_income - bracket_cumulative_income

        return pe.Constraint(
            itertools.product(
                self.sets.all_decision_periods_as_set,
                self.sets.taxing_entities_and_brackets,
            ),
            rule=rule,
        )

    def make_limit_remaining_marginal_income_in_bracket(self):
        def rule(_, t, e, b):
            rem = self.vars.get_remaining_marginal_income_in_bracket(t, e, b)
            ub = self.pars.get_bracket_cumulative_income(e, b)
            return rem <= ub

        return pe.Constraint(
            itertools.product(
                self.sets.all_decision_periods_as_set,
                self.sets.taxing_entities_and_brackets,
            ),
            rule=rule,
        )

    def make_define_taxes_accrued_in_bracket(self):
        def rule(_, t, e, b):
            tax = self.vars.get_taxes_accrued_in_bracket(t, e, b)
            rem = self.vars.get_remaining_marginal_income_in_bracket(t, e, b)
            rate = self.pars.get_bracket_marginal_tax_rate(e, b)
            ub = self.pars.get_bracket_marginal_income(e, b)
            return tax >= (ub - rem) * rate

        return pe.Constraint(
            itertools.product(
                self.sets.all_decision_periods_as_set,
                self.sets.taxing_entities_and_brackets,
            ),
            rule=rule,
        )

    def make_satisfy_retirement_spending_requirement(self):
        def rule(_, t):
            all_withdrawals = sum(
                self.vars.get_withdrawal(i, t)
                for i in self.sets.investments_and_guaranteed_investments
            )
            spending = self.pars.get_minimum_monthly_withdrawals(t)
            violation = self.vars.get_retirement_spending_violation(t)
            return violation >= spending - all_withdrawals

        if not self.sets.investments_and_guaranteed_investments:
            return pe.Constraint.NoConstraint
        else:
            return pe.Constraint(
                itertools.product(self.sets.retirement_periods_as_set), rule=rule
            )

    def make_zero_allocations_for_guaranteed_investments(self):
        def rule(_, i, t):
            if self.pars.get_is_guaranteed_investment(i):
                return self.vars.get_allocation(i, t) == 0
            else:
                return pe.Constraint.Skip

        return pe.Constraint(
            itertools.product(
                self.sets.instruments, self.sets.all_decision_periods_as_set
            ),
            rule=rule,
        )

    def make_define_taxable_monthly_income(self):
        def rule(_, t):
            rrsp_allocations = sum(
                self.vars.get_allocation(i, t)
                for i in self.sets.rrsp_investments_and_guaranteed_investments
            )
            non_tfsa_withdrawals = sum(
                self.vars.get_withdrawal(i, t)
                for i in self.sets.non_tfsa_investments_and_guaranteed_investments
            )
            taxable_income = self.vars.get_taxable_monthly_income(t)
            return taxable_income == (
                self.pars.get_before_tax_monthly_income(t)
                + non_tfsa_withdrawals
                - rrsp_allocations
            )

        return pe.Constraint(self.sets.all_decision_periods_as_set, rule=rule)

    def make_define_rrsp_deduction_limits(self):
        def rule(_, y):
            decision_periods = self.sets.decision_periods.grouped_by_years[y]
            annual_income = sum(
                self.pars.get_before_tax_monthly_income(dp.index)
                for dp in decision_periods
            )
            rrsp_limit = self.pars.get_rrsp_limit(y)
            rrsp_investments = sum(
                self.vars.get_allocation(i, dp.index)
                for i, dp in itertools.product(
                    self.sets.rrsp_investments_and_guaranteed_investments,
                    decision_periods,
                )
            )
            prev_deduction = (
                self.pars.get_starting_rrsp_deduction_limit()
                if y == min(self.sets.years)
                else self.vars.get_rrsp_deduction_limit(y - 1)
            )
            cur_deduction = self.vars.get_rrsp_deduction_limit(y)
            return (
                cur_deduction
                == prev_deduction
                + min(rrsp_limit, annual_income * RRSP_LIMIT_INCOME_FACTOR)
                - rrsp_investments
            )

        return pe.Constraint(self.sets.years, rule=rule)

    def make_set_minimum_rrif_withdrawals(self):
        def rule(_, t):
            max_year = max(self.sets.decision_periods.get_years_in_decision_period(t))
            max_age = floor(self.pars.get_age(max_year))
            max_min_payment_percentage = RRIFMinPaymentCalculator.get_min_payment_percentage(
                max_age
            )
            total_rrsp_balance = sum(
                self.vars.get_balance(i, t)
                for i in self.sets.rrsp_investments_and_guaranteed_investments
            )
            min_withdrawal_fraction = max_min_payment_percentage / 100 / MONTHS_IN_YEAR
            min_rrsp_withdrawal = total_rrsp_balance * min_withdrawal_fraction
            total_rrsp_withdrawals = sum(
                self.vars.get_withdrawal(i, t)
                for i in self.sets.rrsp_investments_and_guaranteed_investments
            )
            return total_rrsp_withdrawals >= min_rrsp_withdrawal

        if self.sets.rrsp_investments_and_guaranteed_investments:
            return pe.Constraint(self.sets.retirement_periods_as_set, rule=rule)
        else:
            return pe.Constraint.NoConstraint

    def make_define_tfsa_deduction_limits(self):
        def get_total_tfsa_withdrawals(y: int):
            if y == min(self.sets.years) - 1:
                return 0
            decision_periods = self.sets.decision_periods.grouped_by_years[y]
            return sum(
                self.vars.get_withdrawal(i, dp.index)
                for i, dp in itertools.product(
                    self.sets.tfsa_investments_and_guaranteed_investments,
                    decision_periods,
                )
            )

        def rule(_, y):
            decision_periods = self.sets.decision_periods.grouped_by_years[y]
            additional_tfsa_limit = self.pars.get_additional_tfsa_limit(y)
            tfsa_investments = sum(
                self.vars.get_allocation(i, dp.index)
                for i, dp in itertools.product(
                    self.sets.tfsa_investments_and_guaranteed_investments,
                    decision_periods,
                )
            )
            prev_deduction = (
                self.pars.get_starting_tfsa_contribution_limit()
                if y == min(self.sets.years)
                else self.vars.get_tfsa_contribution_limit(y - 1)
            )
            last_year_withdrawals = get_total_tfsa_withdrawals(y - 1)
            cur_deduction = self.vars.get_tfsa_contribution_limit(y)
            return (
                cur_deduction
                == prev_deduction
                + additional_tfsa_limit
                + last_year_withdrawals
                - tfsa_investments
            )

        if self.sets.tfsa_investments_and_guaranteed_investments:
            return pe.Constraint(self.sets.years, rule=rule)
        else:
            return pe.Constraint.NoConstraint

    def make_set_withdrawal_limits(self):
        def rule(_, i, t):
            withdrawal = self.vars.get_withdrawal(i, t)
            if self.pars.get_is_guaranteed_investment(
                i
            ) and not self.pars.get_has_guaranteed_investment_matured(i, t):
                return withdrawal == 0
            if self.pars.get_is_rrsp_investment(i) and not self.pars.get_is_retired(t):
                return withdrawal == 0
            return pe.Constraint.Skip

        return pe.Constraint(
            itertools.product(
                self.sets.investments_and_guaranteed_investments,
                self.sets.all_decision_periods_as_set,
            ),
            rule=rule,
        )

    def make_define_surplus_withdrawal_differences(self):
        def rule(_, t):
            if t == 0:
                return pe.Constraint.Skip
            cur_surplus_withdrawal = sum(
                self.vars.get_withdrawal(i, t)
                for i in self.sets.investments_and_guaranteed_investments
            ) - self.pars.get_minimum_monthly_withdrawals(t)
            prev_surplus_withdrawal = sum(
                self.vars.get_withdrawal(i, t - 1)
                for i in self.sets.investments_and_guaranteed_investments
            ) - self.pars.get_minimum_monthly_withdrawals(t - 1)
            pos_difference = self.vars.get_pos_withdrawal_difference(t)
            neg_difference = self.vars.get_neg_withdrawal_difference(t)
            return (
                pos_difference - neg_difference
                == cur_surplus_withdrawal - prev_surplus_withdrawal
            )

        return pe.Constraint(self.sets.all_decision_periods_as_set, rule=rule)

    def make_limit_surplus_withdrawal_fluctuations(self):
        def rule(_):
            total_fluctuation = sum(
                (
                    self.vars.get_pos_withdrawal_difference(t)
                    + self.vars.get_neg_withdrawal_difference(t)
                )
                * self.sets.get_num_months_in_decision_period(t)
                for t in self.sets.all_decision_periods_as_set
            )
            # violation = self.vars.get_withdrawal_fluctuation_violation()
            return (
                total_fluctuation
                <= 6
                * self.pars.user_finances.financial_profile.monthly_retirement_spending
                + 10000
            )

        return pe.Constraint(rule=rule)

    def make_limit_monthly_payment(self):
        def rule(_, i, t):
            max_allocation = self.pars.get_max_monthly_payment(i, t)
            if max_allocation is None:
                return pe.Constraint.Skip
            num_months = self.sets.get_num_months_in_decision_period(t)
            violation = self.vars.get_max_monthly_payment_violation(i, t)
            allocation = self.vars.get_allocation(i, t)
            return violation >= (allocation - max_allocation) * num_months

        return pe.Constraint(
            itertools.product(
                self.sets.instruments, self.sets.all_decision_periods_as_set
            ),
            rule=rule,
        )

    def make_same_mortgage_payments(self):
        def rule(_, m, t):
            if (
                t > self.pars.get_instrument_final_payment_horizon(m).index - 1
                or t == 0
            ):
                return pe.Constraint.Skip

            allocation = self.vars.get_allocation(m, t)
            first = self.vars.get_allocation(m, 0)
            return allocation == first

        return pe.Constraint(
            itertools.product(self.sets.mortgages, self.sets.working_periods_as_set),
            rule=rule,
        )

    def make_penalize_savings_goal_violations(self):
        def rule(_, g, t):
            investments = self.sets.get_allowed_investments_for_goal(g)
            total_balance = sum(self.vars.get_balance(i, t) for i in investments)
            goal_violation = self.vars.get_savings_goal_violation(g, t)
            expected_balance = self.pars.get_goal_amount(g, t)
            return goal_violation >= expected_balance - total_balance

        return pe.Constraint(self.sets.savings_goals_and_decision_periods, rule=rule)

    def make_penalize_purchase_goal_violations(self):
        def rule(_, g):
            investments = self.sets.get_allowed_investments_for_goal(g)
            m = self.pars.get_goal_due_month(g)
            t = self.sets.decision_periods.get_corresponding_period_or_closest(m).index
            num_months_in_dp = self.sets.get_num_months_in_decision_period(t)
            withdrawal = sum(self.vars.get_withdrawal(i, t) for i in investments)
            goal_violation = self.vars.get_purchase_goal_violation(g)
            expected_withdrawal = self.pars.get_goal_amount(g, t)
            return goal_violation >= expected_withdrawal / num_months_in_dp - withdrawal

        return pe.Constraint(self.sets.purchase_goals, rule=rule)


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
    define_taxable_monthly_income: pe.Constraint
    define_rrsp_deduction_limits: pe.Constraint
    set_minimum_rrif_withdrawals: pe.Constraint
    define_tfsa_deduction_limits: pe.Constraint
    set_withdrawal_limits: pe.Constraint
    define_surplus_withdrawal_differences: pe.Constraint
    limit_surplus_withdrawal_fluctuations: pe.Constraint
    limit_monthly_payment: pe.Constraint
    same_mortgage_payments: pe.Constraint
    penalize_purchase_goal_violations: pe.Constraint
    penalize_savings_goal_violations: pe.Constraint

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
            zero_allocations_for_guaranteed_investments=cm.make_zero_allocations_for_guaranteed_investments(),
            define_taxable_monthly_income=cm.make_define_taxable_monthly_income(),
            define_rrsp_deduction_limits=cm.make_define_rrsp_deduction_limits(),
            set_minimum_rrif_withdrawals=cm.make_set_minimum_rrif_withdrawals(),
            define_tfsa_deduction_limits=cm.make_define_tfsa_deduction_limits(),
            set_withdrawal_limits=cm.make_set_withdrawal_limits(),
            define_surplus_withdrawal_differences=cm.make_define_surplus_withdrawal_differences(),
            limit_surplus_withdrawal_fluctuations=cm.make_limit_surplus_withdrawal_fluctuations(),
            limit_monthly_payment=cm.make_limit_monthly_payment(),
            same_mortgage_payments=cm.make_same_mortgage_payments(),
            penalize_purchase_goal_violations=cm.make_penalize_purchase_goal_violations(),
            penalize_savings_goal_violations=cm.make_penalize_savings_goal_violations(),
        )
