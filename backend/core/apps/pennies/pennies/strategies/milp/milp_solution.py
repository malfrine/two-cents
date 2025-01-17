import itertools
import logging
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
from pennies.strategies.milp.utilities import AttributeUtility
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class MILPSolution:
    milp: MILP

    attribute_utility: AttributeUtility = None

    def __post_init__(self):
        self.attribute_utility = AttributeUtility(
            sets=self.milp.sets,
            pars=self.milp.milp_parameters,
            vars=self.milp.variables,
        )

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
            {i: get_withdrawal(i, t) for i in self.sets.investments}
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

    def get_post_tax_monthly_income(self, t):
        pre_tax_income = self.pars.get_before_tax_monthly_income(t)
        tax = sum(
            self.get_taxes_accrued_in_bracket(t, e, b)
            for e, b in self.sets.taxing_entities_and_brackets
        )
        return pre_tax_income - tax

    def get_monthly_allowance(self, t):
        return self.pars.get_savings_fraction(t) * self.get_post_tax_monthly_income(t)

    def get_taxes_accrued_in_bracket(self, t, e, b):
        return pe.value(self.vars.get_taxes_accrued_in_bracket(t, e, b))

    def print_objective_components_breakdown(self):
        c = self.objective.components
        logging.debug(f"Risk violation costs: {pe.value(c.get_risk_violation_costs())}")
        logging.debug(
            f"Retirement spending violation costs: {pe.value(c.get_retirement_spending_violation_cost())}"
        )
        logging.debug(
            f"Loan due date violation costs: {pe.value(c.get_loan_due_date_violation_costs())}"
        )
        logging.debug(
            f"Purchase goal violation costs: {pe.value(c.get_purchase_goal_violation_cost())}"
        )
        logging.debug(
            f"Savings goal violation costs: {pe.value(c.get_savings_goal_violation_cost())}"
        )
        logging.debug(
            f"Min payment violation costs: {pe.value(c.get_min_payment_violation_cost())}"
        )
        logging.debug(f"In Debt utility costs: {pe.value(c.get_in_debt_cost())}")

        # logging.debug(f"Taxes overflow costs: {pe.value(c.get_taxes_overflow_cost())}")
        logging.debug(f"Interest Earned: {pe.value(c.get_interest_earned())}")
        logging.debug(f"Final net worth: {pe.value(c.get_final_net_worth())}")
        logging.debug(f"Total: {pe.value(c.get_obj_rule())}")

    def get_milp_monthly_solutions(self) -> Dict[int, MonthlySolution]:
        monthly_payments = self.get_monthly_payments()
        monthly_withdrawals = self.get_monthly_withdrawals()
        monthly_solutions_dict = dict()
        for dp in self.sets.decision_periods.data:
            dp_month = dp.months[0]
            monthly_allowance = self.get_monthly_allowance(dp.index)
            payments = monthly_payments[dp_month]
            withdrawals = monthly_withdrawals[dp_month]
            total_withdrawals = sum(w for w in withdrawals.values())
            tfsa_withdrawals = sum(
                withdrawals.get(i, 0) for i in self.sets.tfsa_investments
            )
            rrsp_contributions = sum(
                payments.get(i, 0) for i in self.sets.rrsp_investments
            )
            portfolio_instruments = dict()
            for i in self.sets.instruments:
                instrument = self.user_personal_finances.portfolio.get_instrument(
                    i
                ).copy(deep=True)
                if dp.index == 0:
                    instrument.current_balance = self.pars.get_starting_balance(i)
                else:
                    instrument.current_balance = round(
                        pe.value(self.vars.get_balance(i, dp.index - 1)), 2
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
            gross_income = (
                self.pars.get_before_tax_monthly_income(dp.index) + total_withdrawals
            )
            taxable_income = gross_income - tfsa_withdrawals - rrsp_contributions
            ms = MonthlySolution(
                month=dp_month,
                portfolio=portfolio,
                allocation=allocation,
                taxes_paid=taxes_paid,
                withdrawals=withdrawals,
                gross_income=gross_income,
                taxable_income=taxable_income,
            )
            monthly_solutions_dict[dp_month] = ms
        return monthly_solutions_dict
