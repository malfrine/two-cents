import itertools
from dataclasses import dataclass

import pyomo.environ as pe

from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class ObjectiveComponents:
    sets: MILPSets
    pars: MILPParameters
    vars: MILPVariables

    REGISTERED_ACCOUNT_BENEFIT = 0.025
    PREFERENCE_VIOLATION_COST = 1000
    MANDATORY_REQUIREMENT_VIOLATION_COST = 100_000
    # TODO: dynamic violation costs based on user income

    def get_risk_violation_costs(self):
        return self.MANDATORY_REQUIREMENT_VIOLATION_COST * (
            sum(
                self.vars.get_total_risk_violation(t)
                + self.vars.get_investment_risk_violation(t)
                for t in self.sets.working_periods_as_set
            )
        )

    def get_loan_due_date_violation_costs(self):
        return self.MANDATORY_REQUIREMENT_VIOLATION_COST * (
            sum(
                self.vars.get_loan_due_date_violation(l, t)
                for l, t in itertools.product(
                    self.sets.loans, self.sets.working_periods_as_set
                )
            )
        )

    def get_retirement_spending_violation_cost(self):
        return self.MANDATORY_REQUIREMENT_VIOLATION_COST * (
            sum(
                self.vars.get_retirement_spending_violation(t)
                for t in self.sets.retirement_periods_as_set
            )
        )

    def get_final_net_worth(self):
        final_dp_index = self.pars.get_final_decision_period_index()
        return sum(
            self.vars.get_balance(i, final_dp_index) for i in self.sets.instruments
        )

    def get_interest_earned(self):
        return sum(
            self.vars.get_balance(i, t) * (self.pars.get_average_interest_rate(i, t))
            for i, t in itertools.product(
                self.sets.instruments, self.sets.working_periods_as_set
            )
        )

    def get_savings_goal_violation_cost(self):
        return self.PREFERENCE_VIOLATION_COST * sum(
            self.vars.get_savings_goal_violation(g, t)
            for g, t in self.sets.savings_goals_and_decision_periods
        )

    def get_purchase_goal_violation_cost(self):
        return self.PREFERENCE_VIOLATION_COST * sum(
            self.vars.get_purchase_goal_violation(g) for g in self.sets.purchase_goals
        )

    def get_registered_account_incentive(self):
        return self.REGISTERED_ACCOUNT_BENEFIT * sum(
            self.vars.get_allocation(i, t)
            for i, t in itertools.product(
                self.sets.registered_investments, self.sets.working_periods_as_set
            )
        )

    def get_min_payment_violation_cost(self):
        loan_violations = sum(
            self.vars.get_min_payment_violation(l, t)
            for l, t in itertools.product(
                self.sets.loans, self.sets.all_decision_periods_as_set
            )
        )
        investment_violations = sum(
            self.vars.get_min_payment_violation(i, t)
            for i, t in itertools.product(
                self.sets.non_guaranteed_investments,
                self.sets.all_decision_periods_as_set,
            )
        )
        return (
            self.MANDATORY_REQUIREMENT_VIOLATION_COST * loan_violations
            + self.PREFERENCE_VIOLATION_COST * investment_violations
        )

    def get_obj(self):
        obj = (
            -self.get_risk_violation_costs()
            - self.get_loan_due_date_violation_costs()
            - self.get_retirement_spending_violation_cost()
            - self.get_savings_goal_violation_cost()
            - self.get_purchase_goal_violation_cost()
            - self.get_min_payment_violation_cost()
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
        cls, sets: MILPSets, pars: MILPParameters, vars_: MILPVariables,
    ) -> "MILPObjective":
        components = ObjectiveComponents(sets, pars, vars_)
        return MILPObjective(
            obj=pe.Objective(expr=components.get_obj(), sense=pe.maximize,),
            components=components,
        )
