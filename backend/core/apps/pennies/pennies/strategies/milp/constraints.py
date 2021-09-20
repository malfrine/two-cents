import itertools
from dataclasses import dataclass
from typing import List

import pyomo.environ as pe

from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.utilities import AttributeUtility
from pennies.strategies.milp.variables import MILPVariables
from pennies.utilities.finance import calculate_instrument_balance


@dataclass
class _ConstraintMaker:
    sets: MILPSets
    pars: MILPParameters
    vars: MILPVariables

    attribute_utility: AttributeUtility = None

    def __post_init__(self):
        self.attribute_utility = AttributeUtility(
            sets=self.sets, pars=self.pars, vars=self.vars
        )

    def make_define_loan_paid_off_indicator(self) -> pe.Constraint:
        def rule(_, l, t):
            balance = self.vars.get_balance(l, t)
            upper_bound = self.pars.get_loan_upper_bound(l)
            is_unpaid = self.vars.get_is_unpaid(l, t)
            return balance >= upper_bound * is_unpaid

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
            if self.pars.get_is_non_guaranteed_investment(i):
                return violation >= min_payment - allocation
            else:
                # final_payment_order = self.pars.get_final_work_period_index()
                # next_period = min(t + 1, final_payment_order) # TODO: does this need to be removed?
                upper_bound = self.pars.get_allocation_upper_bound(t)
                is_paid_off = 1 - self.vars.get_is_unpaid(i, t)
                allocation_slack = upper_bound * is_paid_off
                return violation >= min_payment - allocation - allocation_slack

        return pe.Constraint(
            itertools.product(self.sets.instruments, self.sets.working_periods_as_set),
            rule=rule,
        )

    def make_define_account_balance(self) -> pe.Constraint:
        def rule(_, i, t):
            cur_balance = self.vars.get_balance(i, t)
            if t == min(self.sets.all_decision_periods_as_set):
                prev_balance = self.pars.get_starting_balance(i)
            else:
                prev_balance = self.vars.get_balance(i, t - 1)

            if self.pars.get_is_investment(i):
                withdrawal = self.vars.get_withdrawal(i, t)
            else:
                withdrawal = 0

            n = self.sets.get_num_months_in_decision_period(t)
            r = self.pars.get_average_interest_rate(i, t)
            allocation = self.vars.get_allocation(i, t)
            return cur_balance == calculate_instrument_balance(
                prev_balance, n, r, withdrawal, allocation
            )

        return pe.Constraint(
            itertools.product(
                self.sets.instruments, self.sets.all_decision_periods_as_set
            ),
            rule=rule,
        )

    def make_total_allocations_limit(self) -> pe.Constraint:
        def rule(_, t):
            post_tax_income = self.attribute_utility.get_post_tax_monthly_income(t)
            total_goal_allocations = self.attribute_utility.get_total_goal_allocations(
                t
            )
            instrument_allocations = self.attribute_utility.get_total_allocations(t)
            savings_fraction = self.pars.get_savings_fraction(t)
            return (
                post_tax_income - total_goal_allocations
            ) * savings_fraction == instrument_allocations

        return pe.Constraint(self.sets.all_decision_periods_as_set, rule=rule)

    def make_loans_are_non_positive(self) -> pe.Constraint:
        def rule(_, i, t):
            if self.pars.get_is_investment(i):
                return self.vars.get_balance(i, t) >= 0
            else:  # is loan
                return self.vars.get_balance(i, t) <= 0

        return pe.Constraint(
            itertools.product(
                self.sets.instruments, self.sets.all_decision_periods_as_set
            ),
            rule=rule,
        )

    def make_pay_off_loans_by_end_date(self) -> pe.Constraint:
        def rule(_, l, t):
            """
            Violation must be greater than the balance. Since loan balances are always negative we have to multiply
            the balance by negative 1
            """
            is_before_end_date = self.pars.get_is_before_loan_due_date(l, t)
            if is_before_end_date:
                return pe.Constraint.Skip
            else:
                violation = self.vars.get_loan_due_date_violation(l, t)
                balance = self.vars.get_balance(l, t)
                return violation >= -balance

        return pe.Constraint(
            itertools.product(self.sets.loans, self.sets.working_periods_as_set),
            rule=rule,
        )

    def make_limit_total_risk(self) -> pe.Constraint:
        def rule(_, t):
            """
            if actual volatility is greater than allowed volatility - model will incur violation penalty
            """
            volatility_limit = self.pars.get_volatility_limit()
            actual_volatility = self.attribute_utility.get_allocation_volatility(t)
            violation = self.vars.get_total_risk_violation(t)
            allowance = self.attribute_utility.get_monthly_allowance(t)
            allowed_volatility = volatility_limit * allowance
            return violation >= actual_volatility - allowed_volatility

        if self.pars.has_investments() and self.pars.has_loans():
            return pe.Constraint(
                itertools.product(self.sets.working_periods_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint

    def make_limit_investment_risk(self) -> pe.Constraint:

        volatility_limit = self.pars.get_volatility_limit()

        def rule(_, t):
            """
            if actual volatility is greater than allowed volatility - model will incur violation penalty
            """
            investment_allocations = self.attribute_utility.get_investment_allocations(
                t
            )
            actual_volatility = self.attribute_utility.get_allocation_volatility(t)
            allowed_volatility = investment_allocations * volatility_limit
            violation = self.vars.get_investment_risk_violation(t)
            return violation >= actual_volatility - allowed_volatility

        if self.pars.has_investments():
            return pe.Constraint(
                itertools.product(self.sets.working_periods_as_set), rule=rule
            )
        else:
            return pe.Constraint.NoConstraint

    def make_define_taxes_accrued_in_bracket(self):
        def rule(_, t, e, b):
            accrued_taxes = self.vars.get_taxes_accrued_in_bracket(t, e, b)
            taxable_income = self.vars.get_taxable_income_in_bracket(t, e, b)
            rate = self.pars.get_bracket_marginal_tax_rate(e, b)
            return accrued_taxes >= taxable_income * rate

        return pe.Constraint(
            itertools.product(
                self.sets.all_decision_periods_as_set,
                self.sets.taxing_entities_and_brackets,
            ),
            rule=rule,
        )

    def make_satisfy_retirement_spending_requirement(self):
        def rule(_, t):
            all_withdrawals = self.attribute_utility.get_all_withdrawals(t)
            spending = self.pars.get_minimum_monthly_withdrawals(t)
            violation = self.vars.get_retirement_spending_violation(t)
            return violation >= spending - all_withdrawals

        if not self.sets.investments:
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
            """We use a greater than sign because the left hand sign can be negative.
            Taxable income must always be non-negative"""
            taxable_withdrawals = self.attribute_utility.get_total_taxable_withdrawals(
                t
            )
            rrsp_allocations = self.attribute_utility.get_rrsp_allocations(t)
            taxable_income = self.vars.get_taxable_monthly_income(t)
            before_tax_monthly_income = self.pars.get_before_tax_monthly_income(t)
            return taxable_income >= (
                before_tax_monthly_income + taxable_withdrawals - rrsp_allocations
            )

        return pe.Constraint(self.sets.all_decision_periods_as_set, rule=rule)

    def make_define_rrsp_deduction_limits(self):
        def rule(_, y):
            """
            rrsp contribution limit in a year is the
                rrsp contribution limit last year
                plus additional growth to the contribution room (based on income, etc.)
                plus any money withdrawn from your rrsp last year
                minus money allocated to rrsps this year

            # TODO: validate the correct years for each variable
            """
            additional_rrsp_limit = self.pars.get_additional_rrsp_limit(y)
            cur_deduction = self.attribute_utility.get_rrsp_contribution_limit(y)
            prev_deduction = self.attribute_utility.get_rrsp_contribution_limit(y - 1)
            last_year_withdrawals = self.attribute_utility.get_annual_rrsp_withdrawals(
                y - 1
            )
            rrsp_allocations = self.attribute_utility.get_annual_rrsp_allocations(y)
            return (
                cur_deduction
                == prev_deduction
                + additional_rrsp_limit
                + last_year_withdrawals
                - rrsp_allocations
            )

        return pe.Constraint(self.sets.years, rule=rule)

    def make_set_minimum_rrif_withdrawals(self):
        def rule(_, t):
            mandatory_withdrawal = self.attribute_utility.get_min_rrif_withdrawal(t)
            total_rrsp_withdrawals = self.attribute_utility.get_total_rrsp_withdrawals(
                t
            )
            return total_rrsp_withdrawals >= mandatory_withdrawal

        if self.pars.has_rrsp_investments():
            return pe.Constraint(self.sets.retirement_periods_as_set, rule=rule)
        else:
            return pe.Constraint.NoConstraint

    def make_define_tfsa_deduction_limits(self):
        def rule(_, y):
            """
            tfsa contribution limit in a year is the
                tfsa contribution limit last year
                plus additional growth to the contribution room (based on income, etc.)
                plus any money withdrawn from your tfsa last year
                minus money allocated to tfsa this year

            # TODO: validate the correct years for each variable
            """
            additional_tfsa_limit = self.pars.get_additional_tfsa_limit(y)
            last_year_withdrawals = self.attribute_utility.get_annual_tfsa_withdrawals(
                y - 1
            )
            cur_deduction = self.attribute_utility.get_tfsa_contribution_limit(y)
            prev_deduction = self.attribute_utility.get_tfsa_contribution_limit(y - 1)
            tfsa_allocations = self.attribute_utility.get_annual_tfsa_allocations(y)
            return (
                cur_deduction
                == prev_deduction
                + additional_tfsa_limit
                + last_year_withdrawals
                - tfsa_allocations
            )

        if self.pars.has_tfsa_investments():
            return pe.Constraint(self.sets.years, rule=rule)
        else:
            return pe.Constraint.NoConstraint

    def make_set_withdrawal_limits(self):
        def rule(_, i, t):
            """
            guaranteed investments that have not matured must not have any withdrawals

            """
            is_guaranteed = self.pars.get_is_guaranteed_investment(i)
            withdrawal = self.vars.get_withdrawal(i, t)
            if not is_guaranteed:
                is_retired = self.pars.get_is_retired(t)
                is_purchase_goal_due = self.pars.get_is_purchase_goal_due(t)
                if is_retired or is_purchase_goal_due:
                    # only allow withdrawals on days that the user is retired or they have to withdraw money for a goal
                    return pe.Constraint.Skip
                else:
                    return withdrawal == 0
            has_matured = self.pars.get_has_guaranteed_investment_matured(i, t)
            if has_matured:
                is_retired = self.pars.get_is_retired(t)
                is_purchase_goal_due = self.pars.get_is_purchase_goal_due(t)
                if is_retired or is_purchase_goal_due:
                    # only allow withdrawals on days that the user is retired or they have to withdraw money for a goal
                    return pe.Constraint.Skip
                else:
                    return withdrawal == 0
            return withdrawal == 0

        return pe.Constraint(
            itertools.product(
                self.sets.investments, self.sets.all_decision_periods_as_set,
            ),
            rule=rule,
        )

    def make_limit_monthly_payment(self):
        def rule(_, i, t):
            max_allocation = self.pars.get_max_monthly_payment(i, t)
            if max_allocation is None:
                return pe.Constraint.Skip
            allocation = self.vars.get_allocation(i, t)
            return allocation <= max_allocation

        return pe.Constraint(
            itertools.product(
                self.sets.instruments, self.sets.all_decision_periods_as_set
            ),
            rule=rule,
        )

    def make_same_mortgage_payments(self):
        def rule(_, m, t):
            is_after_due_date = self.pars.get_is_after_loan_due_date(m, t)
            if is_after_due_date:
                return pe.Constraint.Skip
            allocation = self.vars.get_allocation(m, t)
            first_decision_period = self.sets.decision_periods.min_period_index
            first = self.vars.get_allocation(m, first_decision_period)
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
            """
            we have the spread out the withdrawal over all the months in the decision period
            ideally the decision period size will be 1 month long. so it's not a big deal but just in case

            also, if the due month is outside any of the decision periods, we will pick the closest decision period
            essentially the minimum or maximum month depending on the edge case
            """
            m = self.pars.get_goal_due_month(g)
            t = self.sets.decision_periods.get_corresponding_period_or_closest(m).index
            goal_allocation = self.vars.get_goal_allocation(g)
            goal_violation = self.vars.get_purchase_goal_violation(g)
            expected_goal_allocation = self.attribute_utility.get_expected_goal_allocation(
                g, t
            )
            return goal_violation >= expected_goal_allocation - goal_allocation

        return pe.Constraint(self.sets.purchase_goals, rule=rule)

    def make_taxable_income_upper_bound1(self):
        def rule(_, t, e, b):
            taxable_income = self.vars.get_taxable_income_in_bracket(t, e, b)
            bracket_marginal_income = self.pars.get_bracket_marginal_income(e, b)
            return taxable_income <= bracket_marginal_income

        return pe.Constraint(
            self.sets.all_decision_periods_as_set,
            self.sets.taxing_entities_and_brackets,
            rule=rule,
        )

    def make_taxable_income_upper_bound2(self):
        def rule(_, t, e, b):
            taxable_income = self.vars.get_taxable_income_in_bracket(t, e, b)
            income_surplus = self.attribute_utility.get_income_surplus_over_bracket(
                t, e, b
            )
            return taxable_income <= income_surplus

        return pe.Constraint(
            self.sets.all_decision_periods_as_set,
            self.sets.taxing_entities_and_brackets,
            rule=rule,
        )

    def make_taxable_income_lower_bound1(self):
        def rule(_, t, e, b):
            taxable_income_in_bracket = self.vars.get_taxable_income_in_bracket(t, e, b)
            income_surplus = self.attribute_utility.get_income_surplus_over_bracket(
                t, e, b
            )
            upper_bound = self.pars.get_taxable_income_upper_bound(e, b)
            surplus_greater_than_band = self.vars.get_income_surplus_greater_than_bracket_band(
                t, e, b
            )
            slack = upper_bound * surplus_greater_than_band
            return taxable_income_in_bracket >= income_surplus - slack

        return pe.Constraint(
            self.sets.all_decision_periods_as_set,
            self.sets.taxing_entities_and_brackets,
            rule=rule,
        )

    def make_taxable_income_lower_bound2(self):
        def rule(_, t, e, b):
            taxable_income_in_bracket = self.vars.get_taxable_income_in_bracket(t, e, b)
            bracket_marginal_income = self.pars.get_bracket_marginal_income(e, b)
            upper_bound = self.pars.get_taxable_income_upper_bound(e, b)
            surplus_less_than_band = (
                1 - self.vars.get_income_surplus_greater_than_bracket_band(t, e, b)
            )
            slack = upper_bound * surplus_less_than_band
            return taxable_income_in_bracket >= bracket_marginal_income - slack

        return pe.Constraint(
            self.sets.all_decision_periods_as_set,
            self.sets.taxing_entities_and_brackets,
            rule=rule,
        )

    def make_income_surplus_upper_bound(self):
        def rule(_, t, e, b):
            income_surplus = self.attribute_utility.get_income_surplus_over_bracket(
                t, e, b
            )
            bracket_marginal_income = self.pars.get_bracket_marginal_income(e, b)
            upper_bound = self.pars.get_taxable_income_upper_bound(e, b)
            surplus_greater_than_band = self.vars.get_income_surplus_greater_than_bracket_band(
                t, e, b
            )
            slack = upper_bound * surplus_greater_than_band
            return income_surplus <= bracket_marginal_income + slack

        return pe.Constraint(
            self.sets.all_decision_periods_as_set,
            self.sets.taxing_entities_and_brackets,
            rule=rule,
        )

    def make_bracket_band_upper_bound(self):
        def rule(_, t, e, b):
            income_surplus = self.attribute_utility.get_income_surplus_over_bracket(
                t, e, b
            )
            bracket_marginal_income = self.pars.get_bracket_marginal_income(e, b)
            upper_bound = self.pars.get_taxable_income_upper_bound(e, b)
            surplus_less_than_band = (
                1 - self.vars.get_income_surplus_greater_than_bracket_band(t, e, b)
            )
            slack = upper_bound * surplus_less_than_band
            return bracket_marginal_income <= income_surplus + slack

        return pe.Constraint(
            self.sets.all_decision_periods_as_set,
            self.sets.taxing_entities_and_brackets,
            rule=rule,
        )

    def make_set_annual_rrsp_allocation_limit(self):
        def rule(_, y):
            rrsp_allocations = self.attribute_utility.get_annual_rrsp_allocations(y)
            rrsp_deduction_limit = self.pars.get_additional_rrsp_limit(y)
            return rrsp_allocations <= rrsp_deduction_limit

        if self.pars.has_rrsp_investments():
            return pe.Constraint(self.sets.years, rule=rule)
        else:
            return pe.Constraint.NoConstraint


@dataclass
class MILPConstraints:
    define_loan_paid_off_indicator: pe.Constraint
    allocate_minimum_payments: pe.Constraint
    define_account_balance: pe.Constraint
    total_payments_limit: pe.Constraint
    loans_are_non_positive: pe.Constraint
    pay_off_loans_by_end_date: pe.Constraint
    limit_total_risk: pe.Constraint
    limit_investment_risk: pe.Constraint
    define_taxes_accrued_in_bracket: pe.Constraint
    satisfy_retirement_spending_requirement: pe.Constraint
    zero_allocations_for_guaranteed_investments: pe.Constraint
    define_taxable_monthly_income: pe.Constraint
    define_rrsp_deduction_limits: pe.Constraint
    set_minimum_rrif_withdrawals: pe.Constraint
    define_tfsa_deduction_limits: pe.Constraint
    set_withdrawal_limits: pe.Constraint
    limit_monthly_payment: pe.Constraint
    same_mortgage_payments: pe.Constraint
    penalize_purchase_goal_violations: pe.Constraint
    penalize_savings_goal_violations: pe.Constraint
    bracket_taxable_income_upper_bound1: pe.Constraint
    bracket_taxable_income_upper_bound2: pe.Constraint
    bracket_taxable_income_lower_bound1: pe.Constraint
    bracket_taxable_income_lower_bound2: pe.Constraint
    income_surplus_upper_bound: pe.Constraint
    bracket_band_upper_bound: pe.Constraint
    set_annual_rrsp_allocation_limit: pe.Constraint

    @property
    def as_list(self) -> List[pe.Constraint]:
        return [
            self.define_loan_paid_off_indicator,
            self.allocate_minimum_payments,
            self.define_account_balance,
            self.total_payments_limit,
            self.loans_are_non_positive,
            self.pay_off_loans_by_end_date,
            self.limit_total_risk,
            self.limit_investment_risk,
            self.define_taxes_accrued_in_bracket,
            self.satisfy_retirement_spending_requirement,
            self.zero_allocations_for_guaranteed_investments,
            self.define_taxable_monthly_income,
            self.define_rrsp_deduction_limits,
            self.set_minimum_rrif_withdrawals,
            self.define_tfsa_deduction_limits,
            self.set_withdrawal_limits,
            self.limit_monthly_payment,
            self.same_mortgage_payments,
            self.penalize_purchase_goal_violations,
            self.penalize_savings_goal_violations,
            self.bracket_taxable_income_upper_bound1,
            self.bracket_taxable_income_upper_bound2,
            self.bracket_taxable_income_lower_bound1,
            self.bracket_taxable_income_lower_bound2,
            self.income_surplus_upper_bound,
            self.bracket_band_upper_bound,
            self.set_annual_rrsp_allocation_limit,
        ]

    @classmethod
    def create(
        cls, sets: MILPSets, pars: MILPParameters, vars_: MILPVariables
    ) -> "MILPConstraints":
        cm = _ConstraintMaker(sets=sets, pars=pars, vars=vars_)
        return MILPConstraints(
            define_loan_paid_off_indicator=cm.make_define_loan_paid_off_indicator(),
            allocate_minimum_payments=cm.make_allocate_minimum_payments(),
            define_account_balance=cm.make_define_account_balance(),
            total_payments_limit=cm.make_total_allocations_limit(),
            loans_are_non_positive=cm.make_loans_are_non_positive(),
            pay_off_loans_by_end_date=cm.make_pay_off_loans_by_end_date(),
            limit_total_risk=cm.make_limit_total_risk(),
            limit_investment_risk=cm.make_limit_investment_risk(),
            define_taxes_accrued_in_bracket=cm.make_define_taxes_accrued_in_bracket(),
            satisfy_retirement_spending_requirement=cm.make_satisfy_retirement_spending_requirement(),
            zero_allocations_for_guaranteed_investments=cm.make_zero_allocations_for_guaranteed_investments(),
            define_taxable_monthly_income=cm.make_define_taxable_monthly_income(),
            define_rrsp_deduction_limits=cm.make_define_rrsp_deduction_limits(),
            set_minimum_rrif_withdrawals=cm.make_set_minimum_rrif_withdrawals(),
            define_tfsa_deduction_limits=cm.make_define_tfsa_deduction_limits(),
            set_withdrawal_limits=cm.make_set_withdrawal_limits(),
            limit_monthly_payment=cm.make_limit_monthly_payment(),
            same_mortgage_payments=cm.make_same_mortgage_payments(),
            penalize_purchase_goal_violations=cm.make_penalize_purchase_goal_violations(),
            penalize_savings_goal_violations=cm.make_penalize_savings_goal_violations(),
            bracket_taxable_income_upper_bound1=cm.make_taxable_income_upper_bound1(),
            bracket_taxable_income_upper_bound2=cm.make_taxable_income_upper_bound2(),
            bracket_taxable_income_lower_bound1=cm.make_taxable_income_lower_bound1(),
            bracket_taxable_income_lower_bound2=cm.make_taxable_income_lower_bound2(),
            income_surplus_upper_bound=cm.make_income_surplus_upper_bound(),
            bracket_band_upper_bound=cm.make_bracket_band_upper_bound(),
            set_annual_rrsp_allocation_limit=cm.make_set_annual_rrsp_allocation_limit(),
        )
