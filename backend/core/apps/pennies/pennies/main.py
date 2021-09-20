import logging
import traceback
from typing import Dict

from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.problem_input import ProblemInput
from pennies.model.request import PenniesRequest
from pennies.model.response import PenniesResponse
from pennies.model.solution import Solution, FinancialPlan
from pennies.model.status import PenniesStatus
from pennies.plan_processing.plan import ProcessedFinancialPlan
from pennies.plan_processing.solution import ProcessedSolution
from pennies.plan_processing.solution_processor import SolutionProcessor
from pennies.strategies import get_strategy, StrategyName


def create_plan(problem_input: ProblemInput, strategy_name: str) -> FinancialPlan:
    return get_strategy(strategy_name).create_plan(
        problem_input.user_finances, problem_input.parameters
    )


def create_processed_plan(
    problem_input: ProblemInput, strategy_name: str,
) -> ProcessedFinancialPlan:
    return SolutionProcessor.process_plan(
        create_plan(problem_input, strategy_name), problem_input
    )


def create_solution(problem_input: ProblemInput):
    if problem_input.strategies is None:
        strategies = [StrategyName.investment_milp.value, StrategyName.goal_milp.value]
        if problem_input.user_finances.portfolio.has_loans:
            strategies.append(StrategyName.loan_milp.value)
    else:
        strategies = problem_input.strategies
    plans = {strategy: create_plan(problem_input, strategy) for strategy in strategies}
    # purge none plans
    plans = {strategy: plan for strategy, plan in plans.items() if plan is not None}

    # fail if all plans failed.
    if len(plans.values()) == 0:
        raise ValueError("Not able to solve any plan")

    return Solution(plans=plans, problem_input=problem_input)


def create_processed_solution(problem_input: ProblemInput) -> ProcessedSolution:
    plans = dict()
    if problem_input.strategies is None:
        # dynamically determine appropriate strategies based on user profile
        investment_plan = create_processed_plan(
            problem_input, StrategyName.investment_milp.value
        )
        plans[StrategyName.investment_milp.value] = investment_plan
        if investment_plan is None or investment_plan.has_failed_goal:
            plans[StrategyName.goal_milp.value] = create_processed_plan(
                problem_input, StrategyName.goal_milp.value,
            )
        if problem_input.user_finances.portfolio.has_loans:
            plans[StrategyName.loan_milp.value] = create_processed_plan(
                problem_input, StrategyName.loan_milp.value
            )
    else:
        for strategy_name in problem_input.strategies:
            plans[strategy_name] = create_processed_plan(problem_input, strategy_name)

    # purge none plans
    plans = {strategy: plan for strategy, plan in plans.items() if plan is not None}

    # fail if all plans failed.
    if len(plans.values()) == 0:
        raise ValueError("Not able to solve any plan")

    return ProcessedSolution(plans)


def solve_request(request: Dict) -> Dict:
    try:
        logging.info(request)
        pennies_request = PenniesRequest.parse_obj(request)
        model_input = ProblemInputFactory.from_request(pennies_request)
        solution = create_processed_solution(model_input)
        return PenniesResponse(result=solution, status=PenniesStatus.SUCCESS).dict()

    except Exception:
        logging.error(traceback.format_exc())
        return PenniesResponse(
            result=traceback.format_exc(), status=PenniesStatus.FAILURE
        ).dict()
