from abc import ABC

from pennies.model.parameters import Parameters
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.solution import FinancialPlan


class AllocationStrategy(ABC):
    def create_solution(
        self, user_finances: UserPersonalFinances, parameters: Parameters
    ) -> FinancialPlan:
        ...
