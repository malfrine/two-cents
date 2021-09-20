import json
from pathlib import Path

from pennies.main import create_processed_solution
from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.request import PenniesRequest

PATH_TO_FAILED_REQUEST = Path("tests", "data", "bad_nest_egg_milestone.json")


def test_only_positive_withdrawals():
    d = json.load(open(PATH_TO_FAILED_REQUEST))
    pennies_request = PenniesRequest.parse_obj(d)
    model_input = ProblemInputFactory.from_request(pennies_request)
    create_processed_solution(model_input)
    # for strategy, processed_plan in processed_solution.items():
    #     processed_plan: ProcessedFinancialPlan
    #     goal_failures = [
    #         failure for failure in processed_plan.failures
    #         if failure.failure_type == PlanFailureType.UNSATISFIED_GOAL.value
    #     ]
    #     assert len(goal_failures) == 1
