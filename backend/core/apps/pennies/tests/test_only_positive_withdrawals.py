import json
from math import isclose
from pathlib import Path

from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.request import PenniesRequest
from pennies.plan_processing.solution_processor import SolutionProcessor
from pennies.main import create_solution

PATH_TO_FAILED_REQUEST = Path("tests", "data", "neg_withdrawals_failure.json")


def test_only_positive_withdrawals():
    d = json.load(open(PATH_TO_FAILED_REQUEST))
    pennies_request = PenniesRequest.parse_obj(d)
    model_input = ProblemInputFactory.from_request(pennies_request)
    solution = create_solution(model_input)
    for strategy_name, plan in solution.plans.items():
        for ms in plan.monthly_solutions:
            for id_, value in ms.allocation.payments.items():
                if isclose(value, 0):
                    continue
                instrument = ms.portfolio.get_instrument(id_)
                assert value >= 0, (
                    f"For {strategy_name} strategy, in month {ms.month},"
                    f" allocation for {instrument.name} is negative {value}"
                )
    SolutionProcessor.process_solution(solution)
