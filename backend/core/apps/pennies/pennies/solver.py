import traceback
from typing import Dict

import pyutilib

from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.response import PenniesResponse
from pennies.model.solution import Solution
from pennies.model.status import PenniesStatus
from pennies.solution_processor import SolutionProcessor
from pennies.strategies import get_strategy


def solve_request(request: Dict) -> Dict:
    try:
        pennies_request = PenniesRequest.parse_obj(request)
        model_input = ProblemInputFactory.from_request(pennies_request)
        solution = solve(model_input)
        processed_solution = SolutionProcessor.process(solution)
        return PenniesResponse(
            result=processed_solution, status=PenniesStatus.SUCCESS
        ).dict()

    except Exception as e:
        return PenniesResponse(
            result=traceback.format_exc(), status=PenniesStatus.FAILURE
        ).dict()


def solve(problem_input: ProblemInput) -> Solution:
    plans = dict()
    for strategy_name in problem_input.strategies:
        solution = get_strategy(strategy_name).create_solution(
            problem_input.user_finances
        )
        if solution is None:
            raise ValueError(f"{strategy_name} could not solve")
        plans[strategy_name] = solution
    return Solution(plans=plans)
