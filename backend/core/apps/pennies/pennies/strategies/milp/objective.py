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
                for l, t in itertools.product(self.sets.loans, self.sets.working_periods_as_set)
            )
            * self.pars.get_constraint_violation_penalty()
            / 10
        )

    def get_taxes_paid(self):
        return (
            sum(
                self.vars.get_taxes_accrued_in_bracket(t, e, b)
                for t, (e, b) in
                itertools.product(self.sets.working_periods_as_set, self.sets.taxing_entities_and_brackets)
            )
        )

    def get_taxes_overflow_cost(self):
        return (
            sum(
                self.vars.get_pos_overflow_in_bracket(t, e, b) + self.vars.get_neg_overflow_in_bracket(t, e, b)
                for t, (e, b) in
                itertools.product(self.sets.working_periods_as_set, self.sets.taxing_entities_and_brackets)
            ) * self.pars.get_constraint_violation_penalty() / 1000
        )

    def get_retirement_spending_violation_cost(self):
        return sum(
            self.vars.get_retirement_spending_violation(t)
            for t in self.sets.retirement_periods_as_set
        ) * self.pars.get_constraint_violation_penalty() / 10

    def get_final_net_worth(self):
        return sum(
            self.vars.get_balance(i, self.pars.get_final_decision_period_index())
            for i in itertools.product(self.sets.instruments)
        )

    def get_interest_earned(self):
        return sum(
            self.vars.get_balance(i, t) * (1 + self.pars.get_average_interest_rate(i, t))
            for i, t in itertools.product(
                self.sets.instruments, self.sets.working_periods_as_set
            )
        )

    def get_obj(self):
        obj = (
            - self.get_risk_violation_costs()
            - self.get_loan_due_date_violation_costs()
            - self.get_taxes_paid()
            - self.get_taxes_overflow_cost()
            - self.get_retirement_spending_violation_cost()
        )
        if self.pars.has_investments():
            obj += self.get_final_net_worth()
        else:
            obj += self.get_interest_earned()
        return obj



@dataclass
class MILPObjective:

    obj: pe.Objective
    components: ObjectiveComponents

    @classmethod
    def create(
        cls, sets: MILPSets, pars: MILPParameters, vars_: MILPVariables
    ) -> "MILPObjective":
        components = ObjectiveComponents(sets, pars, vars_)
        return MILPObjective(
            obj=pe.Objective(
                expr=components.get_obj(),
                sense=pe.maximize,
            ),
            components=components
        )
