import traceback
from typing import Dict

import pyutilib

from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.response import PenniesResponse
from pennies.model.solution import Solution
from pennies.model.status import PenniesStatus
from pennies.solution_processor import SolutionProcessor
from pennies.strategies import get_strategy

pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


def solve_request(request: Dict) -> Dict:
    try:
        pennies_request = PenniesRequest.parse_obj(request)
        model_input = ProblemInput.create_from_pennies_request(pennies_request)
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
    plans = {
        strategy_name: get_strategy(strategy_name).create_solution(
            problem_input.problem
        )
        for strategy_name in problem_input.strategies
    }
    return Solution(plans=plans)
