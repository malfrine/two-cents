import itertools
from dataclasses import dataclass

import pyomo.environ as pe

from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables
from pennies.utilities.datetime import MONTHS_IN_YEAR

ANNUALIZED_DISCOUNT_FACTOR = 1.5 / 100


def get_npv_weighting(month: int):
    w = 1 / (1 + ANNUALIZED_DISCOUNT_FACTOR / MONTHS_IN_YEAR) ** month
    return w

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
                for l, t in itertools.product(
                    self.sets.loans, self.sets.working_periods_as_set
                )
            )
            * self.pars.get_constraint_violation_penalty()
            / 10
        )

    def get_taxes_paid(self):
        return sum(
            self.vars.get_taxes_accrued_in_bracket(t, e, b) * get_npv_weighting(m)
            for t, (e, b) in itertools.product(
                self.sets.working_periods_as_set, self.sets.taxing_entities_and_brackets
            ) for m in self.sets.decision_periods.data[t].months
        )

    def get_taxes_overflow_cost(self):
        return sum(
            self.vars.get_pos_overflow_in_bracket(t, e, b)
            for t, (e, b) in itertools.product(
                self.sets.working_periods_as_set, self.sets.taxing_entities_and_brackets
            )
        ) * (1 + 1)

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
            self.vars.get_balance(i, final_dp_index)
            for i in itertools.product(self.sets.instruments)
        ) * get_npv_weighting(final_month)

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
            self.vars.get_withdrawal(i, t) * get_npv_weighting(m)
            for i, t in
            itertools.product(self.sets.investments_and_guaranteed_investments, self.sets.all_decision_periods_as_set)
            for m in self.sets.decision_periods.data[t].months
        )

    def get_obj(self):
        obj = (
            -self.get_risk_violation_costs()
            - self.get_loan_due_date_violation_costs()
            - self.get_taxes_paid()
            - self.get_taxes_overflow_cost()
            - self.get_retirement_spending_violation_cost()
        )
        if self.pars.has_investments():
            obj += self.get_extra_spending_money() + self.get_final_net_worth() * 0.5
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
            components=components,
        )
