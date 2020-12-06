from abc import ABC

from pennies.model.problem import Problem
from pennies.model.solution import FinancialPlan


class AllocationStrategy(ABC):

    def create_solution(self, problem_input: Problem) -> FinancialPlan:
        ...

