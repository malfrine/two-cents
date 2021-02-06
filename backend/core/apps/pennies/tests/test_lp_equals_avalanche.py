import math

from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.processed.plan import ProcessedFinancialPlan
from pennies.model.request import PenniesRequest, RequestLoan, InterestType
from pennies.model.response import PenniesResponse
from pennies.model.status import PenniesStatus
from pennies.solver import solve_request
from pennies.strategies import get_strategy, StrategyName


def test_lp_equals_avalanche():
    request = get_request()

    # assert equality for unprocessed objects
    problem_input = ProblemInputFactory.from_request(request)
    loan = problem_input.user_finances.portfolio.loans[0]
    avalanche_solution = get_strategy(StrategyName.avalanche.value).create_solution(
        problem_input.user_finances
    )
    milp_solution = get_strategy(StrategyName.lp.value).create_solution(
        problem_input.user_finances
    )
    assert len(milp_solution.monthly_solutions) == len(
        avalanche_solution.monthly_solutions
    )
    for milp_ms, avalanche_ms in zip(
        milp_solution.monthly_solutions, avalanche_solution.monthly_solutions
    ):
        milp_payment = milp_ms.allocation.payments.get(loan.name, 0)
        av_payment = milp_ms.allocation.payments.get(loan.name, 0)
        assert math.isclose(milp_payment, av_payment)

    # assert equality for processed objects
    response = PenniesResponse.parse_obj(solve_request(request.dict()))
    assert response.status == PenniesStatus.SUCCESS
    assert isinstance(response.result, dict)
    milp_plan: ProcessedFinancialPlan = response.result.get(StrategyName.lp.value)
    av_plan: ProcessedFinancialPlan = response.result.get(StrategyName.avalanche.value)
    assert len(milp_plan.net_worth.datasets) == len(av_plan.net_worth.datasets)


def get_request() -> PenniesRequest:
    return PenniesRequest(
        financial_profile=FinancialProfile(
            monthly_allowance=2000, years_to_retirement=10
        ),
        loans=[
            RequestLoan(
                name="loan1",
                apr=1,
                current_balance=-1000,
                minimum_monthly_payment=50,
                final_month=60,
                interest_type=InterestType.FIXED,
            )
        ],
        investments=list(),
        strategies=[StrategyName.avalanche.value, StrategyName.lp.value],
    )
