from abc import ABC

from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.solution import FinancialPlan


class AllocationStrategy(ABC):
    def create_solution(self, problem_input: UserPersonalFinances) -> FinancialPlan:
        ...
