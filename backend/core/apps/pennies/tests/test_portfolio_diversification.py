from pennies.model.status import PenniesStatus
from pennies.solver import solve_request
from pennies.utilities.examples import all_requests_as_dicts, only_investments_request


def test_portfolio_diversification():
    request = only_investments_request().dict()
    response = solve_request(request)
    if response["status"] == PenniesStatus.FAILURE:
        assert False
    assert isinstance(response["result"], dict)
    assert len(response["result"]) == len(request["strategies"])
