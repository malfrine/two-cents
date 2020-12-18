from pennies.model.problem_input import ProblemInput
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.solution import Solution
from pennies.solver import solve, process_request
from tests.examples import simple_problem, pennies_request_as_dict


def test_simple_solve():
    sp = simple_problem()
    assert isinstance(sp, UserPersonalFinances)
    mi = ProblemInput(problem=sp, strategies=["avalanche", "linear-program"])
    solution = solve(mi)
    assert isinstance(solution, Solution)


def test_process_request():
    request = pennies_request_as_dict()
    response = process_request(request)
    assert len(response["msg"]["plans"]) == len(request["strategies"])
    assert response["status"] == "success"
