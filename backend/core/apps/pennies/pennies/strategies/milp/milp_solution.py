import itertools
from dataclasses import dataclass
from typing import Dict, List

import pyomo.environ as pe

from pennies.model.portfolio import Portfolio
from pennies.model.solution import MonthlySolution, MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.milp import MILP
from pennies.strategies.milp.objective import MILPObjective
from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class MILPSolution:
    milp: MILP

    @property
    def sets(self) -> MILPSets:
        return self.milp.sets

    @property
    def vars(self) -> MILPVariables:
        return self.milp.variables

    @property
    def objective(self) -> MILPObjective:
        return self.milp.objective

    @property
    def pars(self) -> MILPParameters:
        return self.milp.milp_parameters

    @property
    def user_personal_finances(self) -> UserPersonalFinances:
        return self.milp.user_finances

    def get_total_taxes_paid(self):

        expr = sum(
            self.vars.get_taxes_accrued_in_bracket(t, e, b)
            for t, (e, b) in itertools.product(
                self.sets.all_decision_periods_as_set,
                self.sets.taxing_entities_and_brackets,
            )
            for _ in self.sets.decision_periods.data[t].months
        )

        return pe.value(expr)

    def get_monthly_payments(self) -> List[Dict[str, float]]:
        def get_allocation(i_, t_):
            return pe.value(self.vars.get_allocation(i_, t_))

        return [
            {i: get_allocation(i, t) for i in self.sets.instruments}
            for t in list(sorted(self.sets.all_decision_periods_as_set))
            for _ in range(self.sets.get_num_months_in_decision_period(t))
        ]

    def get_monthly_withdrawals(self) -> List[Dict[str, float]]:
        def get_withdrawal(i_, t_):
            return pe.value(self.vars.get_withdrawal(i_, t_))

        return [
            {
                i: get_withdrawal(i, t)
                for i in self.sets.investments_and_guaranteed_investments
            }
            for t in list(sorted(self.sets.all_decision_periods_as_set))
            for _ in range(self.sets.get_num_months_in_decision_period(t))
        ]

    def get_remaining_marginal_income_in_bracket(
        self, decision_period_index: int, entity: str, bracket: int
    ):
        return pe.value(
            self.vars.get_remaining_marginal_income_in_bracket(
                decision_period_index, entity, bracket
            )
        )

    def get_positive_overflow_in_bracket(
        self, decision_period_index: int, entity: str, bracket: int
    ):
        return pe.value(
            self.vars.get_pos_overflow_in_bracket(
                decision_period_index, entity, bracket
            )
        )

    def print_objective_components_breakdown(self):
        c = self.objective.components
        print(f"Risk violation costs: {pe.value(c.get_risk_violation_costs())}")
        print(
            f"Retirement spending violation costs: {pe.value(c.get_retirement_spending_violation_cost())}"
        )
        print(
            f"Loan due date violation costs: {pe.value(c.get_loan_due_date_violation_costs())}"
        )
        print(f"Taxes paid: {pe.value(c.get_taxes_paid())}")
        print(f"Taxes overflow costs: {pe.value(c.get_taxes_overflow_cost())}")
        # print(f"Withdrawal differences costs: {pe.value(c.get_withdrawal_differences_cost())}")
        print(f"Interest Earned: {pe.value(c.get_interest_earned())}")
        print(f"Final net worth: {pe.value(c.get_final_net_worth())}")
        print(f"Withdrawals: {pe.value(c.get_extra_spending_money())}")
        print(f"Total: {pe.value(c.get_obj())}")

    def get_milp_monthly_solutions(self) -> Dict[int, MonthlySolution]:
        monthly_payments = self.get_monthly_payments()
        monthly_withdrawals = self.get_monthly_withdrawals()
        monthly_solutions_dict = dict()
        for dp in self.sets.decision_periods.data:
            dp_month = dp.months[0]
            monthly_allowance = (
                self.user_personal_finances.financial_profile.get_monthly_allowance(
                    dp_month
                )
            )
            payments = monthly_payments[dp_month]
            withdrawals = monthly_withdrawals[dp_month]
            portfolio_instruments = dict()
            for i in self.sets.instruments:
                instrument = self.user_personal_finances.portfolio.get_instrument(
                    i
                ).copy(deep=True)
                instrument.current_balance = round(
                    pe.value(self.vars.get_balance(i, dp.index)), 2
                )
                portfolio_instruments[i] = instrument
            portfolio = Portfolio(instruments=portfolio_instruments)
            allocation = MonthlyAllocation(
                payments=payments,
                leftover=monthly_allowance
                - sum(payment for payment in payments.values()),
            )
            taxes_paid = sum(
                round(
                    pe.value(self.vars.get_taxes_accrued_in_bracket(dp.index, e, b)), 3
                )
                for e, b in self.sets.taxing_entities_and_brackets
            )
            ms = MonthlySolution(
                month=dp_month,
                portfolio=portfolio,
                allocation=allocation,
                taxes_paid=taxes_paid,
                withdrawals=withdrawals,
            )
            monthly_solutions_dict[dp_month] = ms
        return monthly_solutions_dict