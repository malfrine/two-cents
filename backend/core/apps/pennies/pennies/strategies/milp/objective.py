import itertools
from dataclasses import dataclass

import pyomo.environ as pe

from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables
from pennies.utilities.datetime import MONTHS_IN_YEAR
from pennies.utilities.finance import DiscountFactorCalculator

ANNUALIZED_DISCOUNT_FACTOR = 3 / 100


@dataclass
class ObjectiveComponents:
    sets: MILPSets
    pars: MILPParameters
    vars: MILPVariables
    discount_factor: float

    GOAL_VIOLATION_COST = 100

    # def get_discount_factor(self, instrument, month):
    #     dp_index = self.sets.decision_periods.month_to_period_dict[month].index
    #     growth_rate = self.pars.get_average_interest_rate(instrument, dp_index) + 1
    #     discount_rate = ANNUALIZED_DISCOUNT_FACTOR / 12 + 1
    #     factor = (growth_rate / discount_rate) ** month
    #     return factor
    #
    # def get_npv_weighting(self, month: int):
    #     w = 1 / (1 + self.discount_factor) ** month
    #     return w

    def get_risk_violation_costs(self):
        return (
            sum(
                self.vars.get_total_risk_violation(t)
                + self.vars.get_investment_risk_violation(t)
                for t in self.sets.working_periods_as_set
            )
            * self.pars.get_constraint_violation_penalty()
            / 10
        )

    def get_loan_due_date_violation_costs(self):
        return (
            sum(
                self.vars.get_loan_due_date_violation(l, t)
                for l, t in itertools.product(
                    self.sets.loans, self.sets.working_periods_as_set
                )
            )
            * self.pars.get_constraint_violation_penalty()
            / 10
        )

    def get_taxes_paid(self):
        return sum(
            self.vars.get_taxes_accrued_in_bracket(t, e, b)
            for t, (e, b) in itertools.product(
                self.sets.all_decision_periods_as_set, self.sets.taxing_entities_and_brackets
            ) for m in self.sets.decision_periods.data[t].months
        )

    def get_taxes_overflow_cost(self):
        return sum(
            self.vars.get_pos_overflow_in_bracket(t, e, b)
            for t, (e, b) in itertools.product(
                self.sets.all_decision_periods_as_set, self.sets.taxing_entities_and_brackets
            )
        ) * (self.pars.get_constraint_violation_penalty())

    def get_retirement_spending_violation_cost(self):
        return (
            sum(
                self.vars.get_retirement_spending_violation(t)
                for t in self.sets.retirement_periods_as_set
            )
            * self.pars.get_constraint_violation_penalty()
            / 10
        )

    def get_final_net_worth(self):
        final_dp_index = self.pars.get_final_decision_period_index()
        final_month = max(self.sets.decision_periods.data[final_dp_index].months)

        return sum(
            self.vars.get_balance(i, final_dp_index) # * self.get_discount_factor(i, final_month)
            for i in self.sets.instruments
        )

    def get_interest_earned(self):
        return sum(
            self.vars.get_balance(i, t)
            * (1 + self.pars.get_average_interest_rate(i, t))
            for i, t in itertools.product(
                self.sets.instruments, self.sets.working_periods_as_set
            )
        )

    def get_extra_spending_money(self):

        return sum(
            self.vars.get_withdrawal(i, t) # * self.get_discount_factor(i, m)
            for i, t in
            itertools.product(self.sets.investments_and_guaranteed_investments, self.sets.all_decision_periods_as_set)
            for m in self.sets.decision_periods.data[t].months
        )

    def get_withdrawal_fluctuation_cost(self):
        return self.vars.get_withdrawal_fluctuation_violation()

    def get_max_payment_violation_cost(self):
        return sum(
            self.vars.get_max_monthly_payment_violation(i, t)
            for i, t in itertools.product(self.sets.instruments, self.sets.all_decision_periods_as_set)
        )

    def get_savings_goal_violation_cost(self):
        return (self.GOAL_VIOLATION_COST + 10) * sum(
            self.vars.get_savings_goal_violation(g, t)
            for g, t in self.sets.savings_goals_and_decision_periods
        )

    def get_purchase_goal_violation_cost(self):
        max_month = self.sets.decision_periods.max_month
        return max_month * self.GOAL_VIOLATION_COST * sum(
            self.vars.get_purchase_goal_violation(g)
            for g in self.sets.purchase_goals
        )

    def get_registered_account_incentive(self):
        return 0.01 * sum(
            self.vars.get_allocation(i, t)
            for i, t in itertools.product(self.sets.registered_investments, self.sets.working_periods_as_set)
        )

    def get_obj(self):
        obj = (
            - self.get_risk_violation_costs()
            - self.get_loan_due_date_violation_costs()
            - self.get_taxes_paid()
            - self.get_taxes_overflow_cost()
            - self.get_retirement_spending_violation_cost()
            - self.get_max_payment_violation_cost()
            - self.get_savings_goal_violation_cost()
            - self.get_purchase_goal_violation_cost()
        )
        if self.pars.has_investments():
            obj += self.get_final_net_worth() + self.get_registered_account_incentive()
        else:
            obj += self.get_interest_earned()
        return obj


@dataclass
class MILPObjective:

    obj: pe.Objective
    components: ObjectiveComponents

    @classmethod
    def create(
        cls, sets: MILPSets, pars: MILPParameters, vars_: MILPVariables, discount_factor: float
    ) -> "MILPObjective":
        components = ObjectiveComponents(sets, pars, vars_, discount_factor)
        return MILPObjective(
            obj=pe.Objective(
                expr=components.get_obj(),
                sense=pe.maximize,
            ),
            components=components,
        )
