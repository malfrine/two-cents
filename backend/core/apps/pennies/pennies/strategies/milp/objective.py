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
        return MILPObjective(
            obj=pe.Objective(
                expr=sum(
                    vars_.get_balance(i, t) * pars.get_average_interest_rate(i, t)
                    for i, t in itertools.product(
                        sets.instruments, sets.payment_horizons_as_set
                    )
                ),
                sense=pe.maximize,
            )
        )
