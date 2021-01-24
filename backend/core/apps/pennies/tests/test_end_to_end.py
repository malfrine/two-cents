from pennies.model.problem_input import ProblemInput
from pennies.model.processed.solution import ProcessedSolution
from pennies.model.status import PenniesStatus
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.solution import Solution
from pennies.solver import solve, solve_request
from tests.examples import simple_problem, pennies_request_as_dict


def test_simple_solve():
    sp = simple_problem()
    assert isinstance(sp, UserPersonalFinances)
    mi = ProblemInput(problem=sp, strategies=["avalanche", "linear-program"])
    solution = solve(mi)
    assert isinstance(solution, Solution)


def test_process_request():
    request = pennies_request_as_dict()
    response = solve_request(request)
    if response["status"] == PenniesStatus.FAILURE:
        print(response["result"])
        assert False
    assert isinstance(response["result"], dict)
    assert len(response["result"]) == len(request["strategies"])
    assert len(response["result"]["linear-program"]["milestones"]) >= len(
        request["loans"]
    )
