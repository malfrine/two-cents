import logging
import os
from pathlib import Path

from pennies.model.status import PenniesStatus
from pennies.main import solve_request
from pennies.strategies import StrategyName
from tests.test_end_to_end import JSONDao

PATH_TO_DATA = Path("tests", "data")


def _assert_successful_solve(f: str):
    json_dao = JSONDao(data_dir=PATH_TO_DATA)
    logging.debug(f"Testing request from file {f}")
    request = json_dao.read_request(f).dict()

    # pennies_request = PenniesRequest.parse_obj(request)
    # assert_correct_milp_calculations(pennies_request)

    response = solve_request(request)
    assert (
        response["status"] == PenniesStatus.SUCCESS
    ), f"failed {f} with {response['result']}"
    assert isinstance(response["result"], dict)
    assert len(response["result"]) == len(request["strategies"])
    assert len(
        response["result"][StrategyName.two_cents_milp.value]["milestones"]
    ) >= len(request["loans"])


def test_process_all_failed_requests():
    failed_request_files = os.listdir(PATH_TO_DATA)
    for f in failed_request_files:
        _assert_successful_solve(f)


def test_fail_request():
    _assert_successful_solve("fail10.json")
