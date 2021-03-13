import pyutilib

from pennies.model.factories.financial_plan import FinancialPlanFactory
from pennies.model.parameters import Parameters
from pennies.model.solution import FinancialPlan
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.allocation_strategy import AllocationStrategy
from pennies.strategies.milp.milp import MILP
from pennies.strategies.milp.milp_solution import MILPSolution

pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


class MILPStrategy(AllocationStrategy):
    def create_solution(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> FinancialPlan:
        milp = MILP.create(user_finances=user_finances, parameters=parameters).solve()
        if milp is None:
            return
        solution = MILPSolution(milp=milp)
        solution.print_objective_components_breakdown()
        return FinancialPlanFactory.create(
            solution.get_monthly_payments(),
            user_finances,
            parameters,
            solution.get_monthly_withdrawals(),
        )
