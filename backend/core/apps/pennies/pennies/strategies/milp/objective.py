import itertools
from dataclasses import dataclass

import pyomo.environ as pe

from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class MILPObjective:

    obj: pe.Objective

    @classmethod
    def create(
        cls, sets: MILPSets, pars: MILPParameters, vars_: MILPVariables
    ) -> "MILPObjective":

        final_net_worth = sum(
            vars_.get_balance(i, pars.get_last_payment_horizon_order())
            for i in itertools.product(sets.instruments)
        )

        interest_earned = sum(
            vars_.get_balance(i, t) * (1 + pars.get_average_interest_rate(i, t))
            for i, t in itertools.product(
                sets.instruments, sets.payment_horizons_as_set
            )
        )

        risk_violation_costs = (
            sum(
                vars_.get_total_risk_violation(t)
                + vars_.get_investment_risk_violation(t)
                for t in sets.payment_horizons_as_set
            )
            * pars.get_constraint_violation_penalty()
            / 100
        )

        loan_due_date_violation_cost = (
            sum(
                vars_.get_loan_due_date_violation(l, t)
                for l, t in itertools.product(sets.loans, sets.payment_horizons_as_set)
            )
            * pars.get_constraint_violation_penalty()
            / 10
        )

        return MILPObjective(
            obj=pe.Objective(
                expr=final_net_worth
                + interest_earned
                - risk_violation_costs
                - loan_due_date_violation_cost,
                sense=pe.maximize,
            )
        )
