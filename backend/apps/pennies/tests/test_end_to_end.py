from pennies.model.model_input import ModelInput
from pennies.model.problem import Problem
from pennies.model.solution import Solution
from pennies.solver import solve, process_request
from tests.examples import simple_problem, pennies_request_as_dict


def test_simple_solve():
    sp = simple_problem()
    assert isinstance(sp, Problem)
    mi = ModelInput(problem=sp, strategies=["avalanche"])
    solution = solve(mi)
    assert isinstance(solution, Solution)

def test_process_request():
    request = pennies_request_as_dict()
    response = process_request(request)
    assert len(response["msg"]["plans"]) == len(request["strategies"])
    assert response["status"] == "success"
