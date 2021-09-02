import itertools
from dataclasses import dataclass
from math import ceil
from uuid import UUID

from pennies.model.rrsp import RRIFMinPaymentCalculator
from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables
from pennies.utilities.datetime import MONTHS_IN_YEAR
from pennies.utilities.finance import estimate_taxable_withdrawal


# G = S + W
# PT = S + W - T
# A = PT - W
# A = S + W - T - W
# A = S - T


@dataclass
class AttributeUtility:
    """A utility to get certain variables and parameters of the MIP"""

    sets: MILPSets
    pars: MILPParameters
    vars: MILPVariables

    def get_total_tax(self, decision_period: int):
        return sum(
            self.vars.get_taxes_accrued_in_bracket(decision_period, e, b)
            for e, b in self.sets.taxing_entities_and_brackets
        )

    def estimate_taxable_withdrawal(self, investment_id: UUID, decision_period: int):
        final_withdrawal_month = max(self.sets.get_months_in_horizon(decision_period))
        starting_month = self.sets.decision_periods.min_month
        months = list(range(starting_month, final_withdrawal_month))
        investment = self.pars.get_investment(investment_id)
        withdrawal = self.vars.get_withdrawal(investment_id, decision_period)
        return estimate_taxable_withdrawal(investment, withdrawal, months)

    def get_total_taxable_withdrawals(self, decision_period: int):
        return sum(
            self.estimate_taxable_withdrawal(i, decision_period)
            for i in self.sets.investments
        )

    def get_gross_monthly_income(self, decision_period: int):
        """
        actual salary + withdrawals from investments
        """
        pre_tax_monthly_income = self.pars.get_before_tax_monthly_income(
            decision_period
        )
        total_withdrawals = self.get_all_withdrawals(decision_period)
        return pre_tax_monthly_income + total_withdrawals

    def get_post_tax_monthly_income(self, decision_period: int):
        total_tax = self.get_total_tax(decision_period)
        gross_income = self.get_gross_monthly_income(decision_period)
        return gross_income - total_tax

    def get_monthly_allowance(self, decision_period: int):
        """
        spendable_income = all the income after taxes - withdrawals
        allowance = spendable_income * savings_fraction
        * withdrawals are usually for something specific so they can't be re-invested back into allocations
        * the rest of their spendable income is on mandatory spending
        """
        post_tax_income = self.get_post_tax_monthly_income(decision_period)
        savings_fraction = self.pars.get_savings_fraction(decision_period)
        return savings_fraction * post_tax_income

    def get_total_allocations(self, decision_period: int):
        return self.vars.get_allocations(self.sets.instruments, [decision_period])

    def get_investment_allocations(self, decision_period: int):
        return self.vars.get_allocations(self.sets.investments, [decision_period])

    def get_allocation_volatility(self, decision_period: int):
        """
        only need to get volatility for non guaranteed investments
        the volatility of all other investments is 0
        """
        return sum(
            self.vars.get_allocation(i, decision_period)
            * self.pars.get_instrument_volatility(i)
            for i in self.sets.non_guaranteed_investments
        )

    def get_all_withdrawals(self, decision_period: int):
        return self.vars.get_withdrawals(self.sets.investments, [decision_period])

    def get_rrsp_allocations(self, decision_period: int):
        return self.vars.get_allocations(self.sets.rrsp_investments, [decision_period])

    def get_annual_rrsp_allocations(self, year: int):
        decision_periods = self.sets.decision_periods.get_indices_of_decision_period_instance_in_year(
            year
        )
        return self.vars.get_allocations(self.sets.rrsp_investments, decision_periods)

    def get_annual_tfsa_allocations(self, year: int):
        decision_periods = self.sets.decision_periods.get_indices_of_decision_period_instance_in_year(
            year
        )
        return self.vars.get_allocations(self.sets.tfsa_investments, decision_periods)

    def get_total_rrsp_withdrawals(self, decision_period: int):
        return self.vars.get_withdrawals(self.sets.rrsp_investments, [decision_period])

    def get_annual_rrsp_withdrawals(self, year: int):
        if year <= min(self.sets.years) - 1:
            return 0
        decision_periods = self.sets.decision_periods.get_indices_of_decision_period_instance_in_year(
            year
        )
        return self.vars.get_withdrawals(self.sets.rrsp_investments, decision_periods)

    def get_rrsp_contribution_limit(self, year: int):
        if year <= min(self.sets.years) - 1:
            return self.pars.get_starting_rrsp_deduction_limit()
        else:
            return self.vars.get_rrsp_deduction_limit(year)

    def get_total_rrsp_balance(self, decision_period: int):
        return sum(
            self.vars.get_balance(i, decision_period)
            for i in self.sets.rrsp_investments
        )

    def get_min_rrif_withdrawal(self, decision_period: int):
        """
        the min rrif withdrawal is based on their age. as the years go up - the min amount goes up.

        since the decision period can last multiple years, we pick the latest possible year
        (to get the latest possible age) so that we can get the maximum required withdrawal in the decision period

        based off of their age, we get the min withdrawal fraction
        the min withdrawal amount is based on the the current balance of the rrif in the decision period
        """
        max_year = max(
            self.sets.decision_periods.get_years_in_decision_period(decision_period)
        )
        max_age = int(ceil(self.pars.get_age(max_year)))
        payment_percentage = RRIFMinPaymentCalculator.get_min_payment_percentage(
            max_age
        )
        total_rrsp_balance = self.get_total_rrsp_balance(decision_period)
        min_withdrawal_fraction = payment_percentage / 100 / MONTHS_IN_YEAR
        return total_rrsp_balance * min_withdrawal_fraction

    def get_annual_tfsa_withdrawals(self, year: int):
        if year <= min(self.sets.years) - 1:
            return 0
        decision_periods = self.sets.decision_periods.grouped_by_years[year]
        return sum(
            self.vars.get_withdrawal(i, dp.index)
            for i, dp in itertools.product(
                self.sets.tfsa_investments, decision_periods,
            )
        )

    def get_tfsa_contribution_limit(self, year: int):
        if year <= min(self.sets.years) - 1:
            return self.pars.get_starting_tfsa_contribution_limit()
        else:
            return self.vars.get_tfsa_contribution_limit(year)

    def get_expected_goal_allocation(self, goal_id: UUID, decision_period: int):
        m = self.pars.get_goal_due_month(goal_id)
        t = self.sets.decision_periods.get_corresponding_period_or_closest(m).index
        num_months_in_dp = self.sets.get_num_months_in_decision_period(t)
        total_goal_amount = self.pars.get_goal_amount(goal_id, decision_period)
        return total_goal_amount / num_months_in_dp

    def get_income_surplus_over_bracket(self, t, e, b):
        monthly_taxable_income = self.vars.get_taxable_monthly_income(t)
        previous_bracket_cumulative_income = self.pars.get_previous_bracket_cumulative_income(
            e, b
        )
        return monthly_taxable_income - previous_bracket_cumulative_income

    def get_total_goal_allocations(self, decision_period: int):
        total_allocations = 0
        for g in self.sets.purchase_goals:
            goal_period = self.pars.get_goal_decision_period(g)
            if decision_period == goal_period:
                goal_allocation = self.vars.get_goal_allocation(g)
                total_allocations += goal_allocation
        return total_allocations
