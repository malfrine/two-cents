from dataclasses import dataclass

from pennies.model.parameters import Parameters
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.constraints import MILPConstraints
from pennies.strategies.milp.objective import MILPObjective
from pennies.strategies.milp.parameters import MILPParameters
from pennies.strategies.milp.sets import MILPSets
from pennies.strategies.milp.variables import MILPVariables


@dataclass
class MILPComponents:
    """A holder for all the MILP components"""

    sets: MILPSets
    parameters: MILPParameters
    variables: MILPVariables
    constraints: MILPConstraints
    objective: MILPObjective

    @classmethod
    def create(cls, user_finances: UserPersonalFinances, parameters: Parameters):
        sets = MILPSets.create(
            user_finances,
            parameters.max_months_in_payment_horizon,
            parameters.max_months_in_retirement_period,
            parameters.starting_month,
        )
        milp_parameters = MILPParameters(user_finances, sets, parameters)
        variables = MILPVariables.create(user_finances, sets)
        constraints = MILPConstraints.create(sets, milp_parameters, variables)
        objective = MILPObjective.create(sets, milp_parameters, variables,)
        return cls(
            sets=sets,
            parameters=milp_parameters,
            variables=variables,
            constraints=constraints,
            objective=objective,
        )
