import logging
import traceback
from typing import Dict

from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.response import PenniesResponse
from pennies.model.solution import Solution
from pennies.model.status import PenniesStatus
from pennies.solution_processor import SolutionProcessor
from pennies.strategies import get_strategy


def solve_request(request: Dict) -> Dict:
    try:
        logging.info(request)
        pennies_request = PenniesRequest.parse_obj(request)
        model_input = ProblemInputFactory.from_request(pennies_request)
        solution = solve(model_input)
        processed_solution = SolutionProcessor.process(solution)
        return PenniesResponse(
            result=processed_solution, status=PenniesStatus.SUCCESS
        ).dict()

    except Exception as e:
        logging.error(traceback.format_exc())
        return PenniesResponse(
            result=traceback.format_exc(), status=PenniesStatus.FAILURE
        ).dict()


def solve(problem_input: ProblemInput) -> Solution:
    plans = dict()
    print(str(problem_input.user_finances))
    for strategy_name in problem_input.strategies:
        plan = get_strategy(strategy_name).create_solution(
            problem_input.user_finances, problem_input.parameters
        )
        if plan is None:
            raise ValueError(f"{strategy_name} could not solve")
        plans[strategy_name] = plan
    for strategy_name, plan in plans.items():
        logging.debug(f"solution strategy: {strategy_name}")
        logging.debug(f"\t net worth: {plan.get_net_worth()}")
        logging.debug(f"\t interest paid on loans: {plan.get_total_interest_paid_on_loans()}")
        logging.debug(
            f"\t interest earned on investments: {plan.get_total_interest_earned_on_investments()}"
        )
        logging.debug(f"\t total withdrawals: {plan.get_total_withdrawals()}")
        logging.debug(f"\t total taxes paid: {plan.get_total_income_taxes_paid()}")

    return Solution(plans=plans, problem_input=problem_input)
