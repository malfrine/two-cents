import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel

from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.status import PenniesStatus
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.solution import Solution
from pennies.solver import solve, solve_request
from pennies.strategies import StrategyName
from pennies.utilities.examples import simple_problem, pennies_request_as_dict

PATH_TO_DATA = Path("tests", "data")


@dataclass
class JSONDao:
    data_dir: Path

    def read_base_model(self, base: ClassVar[BaseModel], filename: str):
        with open(str(Path(self.data_dir, filename))) as f:
            return base.parse_obj(json.load(f))

    def read_request(self, filename: str) -> PenniesRequest:
        return self.read_base_model(PenniesRequest, filename)


def test_simple_solve():
    sp = simple_problem()
    assert isinstance(sp, UserPersonalFinances)
    mi = ProblemInput(
        problem=sp, strategies=[StrategyName.avalanche.value, StrategyName.lp.value]
    )
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
    assert len(response["result"][StrategyName.lp.value]["milestones"]) >= len(
        request["loans"]
    )


def test_process_all_failed_requests():
    failed_request_files = os.listdir(PATH_TO_DATA)
    json_dao = JSONDao(data_dir=PATH_TO_DATA)
    for f in failed_request_files:
        print(f"Testing request from file {f}")
        request = json_dao.read_request(f).dict()
        response = solve_request(request)
        if response["status"] == PenniesStatus.FAILURE:
            print(response["result"])
            assert False
        assert isinstance(response["result"], dict)
        assert len(response["result"]) == len(request["strategies"])
        assert len(response["result"][StrategyName.lp.value]["milestones"]) >= len(
            request["loans"]
        )
