import pyutilib

from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.solution import Solution
from pennies.strategies import get_strategy

pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


def process_request(request):
    if request:
        try:
            print(request)
            pennies_request = PenniesRequest.parse_obj(request)
            # return pennies_request
            model_input = ProblemInput.create_from_pennies_request(pennies_request)
            solution = solve(model_input)
            print(solution)
            return {"status": "success", "msg": solution.dict()}
        except Exception as e:
            raise e
            return {"status": "fail", "msg": str(e)}
            
    return {"msg": "empty request"}


def solve(problem_input: ProblemInput) -> Solution:
    plans = {
        strategy_name: get_strategy(strategy_name).create_solution(
            problem_input.problem
        )
        for strategy_name in problem_input.strategies
    }
    return Solution(plans=plans)
