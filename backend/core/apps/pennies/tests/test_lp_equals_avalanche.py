import math

from pennies.model.constants import Province
from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.interest_rate import FixedLoanInterestRate
from pennies.model.loan import PersonalLoan
from pennies.model.parameters import Parameters
from pennies.plan_processing.plan import ProcessedFinancialPlan
from pennies.model.request import PenniesRequest
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
        problem_input.user_finances, Parameters()
    )
    milp_solution = get_strategy(StrategyName.lp.value).create_solution(
        problem_input.user_finances, Parameters()
    )
    assert len(milp_solution.monthly_solutions) == len(
        avalanche_solution.monthly_solutions
    )
    for milp_ms, avalanche_ms in zip(
        milp_solution.monthly_solutions, avalanche_solution.monthly_solutions
    ):
        milp_payment = milp_ms.allocation.payments.get(loan.id_, 0)
        av_payment = milp_ms.allocation.payments.get(loan.id_, 0)
        assert math.isclose(milp_payment, av_payment)

    # assert equality for plan_processing objects
    response = PenniesResponse.parse_obj(solve_request(request.dict()))
    assert response.status == PenniesStatus.SUCCESS
    assert isinstance(response.result, dict)
    milp_plan: ProcessedFinancialPlan = response.result.get(StrategyName.lp.value)
    av_plan: ProcessedFinancialPlan = response.result.get(StrategyName.avalanche.value)
    assert len(milp_plan.net_worth.datasets) == len(av_plan.net_worth.datasets)


def get_request() -> PenniesRequest:
    return PenniesRequest(
        financial_profile=FinancialProfile(
            monthly_salary_before_tax=2000,
            years_to_retirement=10,
            years_to_death=20,
            percent_salary_for_spending=100,
            province_of_residence=Province.AB,
            starting_tfsa_contribution_limit=0,
            starting_rrsp_contribution_limit=0,
            current_age=50,
            risk_tolerance=0,
        ),
        loans=[
            PersonalLoan(
                name="loan1",
                interest_rate=FixedLoanInterestRate(apr=1),
                current_balance=-50_000,
                minimum_monthly_payment=854,
                final_month=60,
            )
        ],
        investments=list(),
        strategies=[StrategyName.avalanche.value, StrategyName.lp.value],
        goals=list(),
    )
