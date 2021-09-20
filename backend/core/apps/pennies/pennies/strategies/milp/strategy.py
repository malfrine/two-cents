from typing import List, Optional

import pyutilib
import pyomo.environ as pe

from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.parameters import Parameters
from pennies.model.solution import FinancialPlan
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.allocation_strategy import PlanningStrategy
from pennies.strategies.milp.components import MILPComponents
from pennies.strategies.milp.milp import MILP
from pennies.strategies.milp.milp_solution import MILPSolution
from pennies.strategies.milp.utilities import ConcreteModelBuilder

pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


class MILPStrategy(PlanningStrategy):
    def create_plan(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> Optional[FinancialPlan]:
        parameters = self.overwrite_parameters(parameters)
        milp_components = MILPComponents.create(
            user_finances=user_finances, parameters=parameters
        )
        builder = ConcreteModelBuilder()
        pyomo_model = builder.build(
            constraints=self.get_active_constraints(milp_components),
            variables=self.get_active_variables(milp_components),
            objective=milp_components.objective.obj,
        )
        milp = MILP(
            user_finances=user_finances,
            problem_parameters=parameters,
            pyomodel=pyomo_model,
            components=milp_components,
        )
        is_success = milp.solve()
        if not is_success:
            return None
        solution = MILPSolution(milp=milp)
        solution.print_objective_components_breakdown()
        return FinancialPlanFactory.create(
            solution.get_monthly_payments(),
            user_finances,
            parameters,
            solution.get_monthly_withdrawals(),
        )

    def get_active_constraints(
        self, milp_components: MILPComponents
    ) -> List[pe.Constraint]:
        return milp_components.constraints.as_list

    def get_active_variables(self, milp_components: MILPComponents) -> List[pe.Var]:
        return milp_components.variables.as_list

    def overwrite_parameters(self, parameters: Parameters) -> Parameters:
        return parameters


class InvestmentMILPStrategy(MILPStrategy):
    """same as the default MILP strategy"""

    pass


class LoanMILPStrategy(MILPStrategy):

    DEBT_UTILITY_COST = 0.5

    def overwrite_parameters(self, parameters: Parameters) -> Parameters:
        parameters.debt_utility_cost = self.DEBT_UTILITY_COST
        return parameters


class GoalMILPStrategy(MILPStrategy):

    GOAL_VIOLATION_COST = 0.5

    def overwrite_parameters(self, parameters: Parameters) -> Parameters:
        parameters.goal_violation_cost = self.GOAL_VIOLATION_COST
        return parameters
