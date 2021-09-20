import json
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel

from pennies.main import create_processed_solution, solve_request
from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.status import PenniesStatus
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies import StrategyName
from pennies.utilities.examples import (
    simple_user_finances,
    all_requests_as_dicts,
)


@dataclass
class JSONDao:
    data_dir: Path

    def read_base_model(self, base: ClassVar[BaseModel], filename: str):
        with open(str(Path(self.data_dir, filename))) as f:
            j = json.load(f)
            return base.parse_obj(j)

    def read_request(self, filename: str) -> PenniesRequest:
        return self.read_base_model(PenniesRequest, filename)


def test_simple_solve():
    sp = simple_user_finances()
    assert isinstance(sp, UserPersonalFinances)
    mi = ProblemInput(
        user_finances=sp,
        strategies=[StrategyName.avalanche.value, StrategyName.two_cents_milp.value],
    )
    solution = create_processed_solution(mi)
    assert isinstance(solution, dict)


def test_process_all_example_requests():
    for request in all_requests_as_dicts():
        response = solve_request(request)
        print(request)
        assert response["status"] == PenniesStatus.SUCCESS, response["result"]
        assert isinstance(response["result"], dict)
        assert len(response["result"]) == len(request["strategies"])
        assert len(
            response["result"][StrategyName.two_cents_milp.value]["milestones"]
        ) >= len(request["loans"])
