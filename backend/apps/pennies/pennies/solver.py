import pyutilib

from pennies.model.model_input import ModelInput
from pennies.model.request import PenniesRequest
from pennies.model.solution import Solution
from pennies.strategies import get_strategy
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


def process_request(request):
    if request:
        try:
            print(request)
            pennies_request = PenniesRequest.parse_obj(request)
            model_input = ModelInput.create_from_pennies_request(pennies_request)
            solution = solve(model_input)
            print(solution)
            return {
                "status": "success",
                "msg": solution.dict()
            }
        except Exception as e:
            return {"status": "fail", "msg": str(e)}
    return {"msg": "empty request"}


def solve(model_input: ModelInput) -> Solution:
    plans = {
        strategy_name: get_strategy(strategy_name).create_solution(model_input.problem)
        for strategy_name in model_input.strategies
    }
    return Solution(plans=plans)


