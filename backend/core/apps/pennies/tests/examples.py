from typing import Tuple, Dict

from pennies.model.financial_profile import FinancialProfile
from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.problem_input import ProblemInput
from pennies.model.portfolio import Portfolio
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.model.request import PenniesRequest
from pennies.model.solution import MonthlyAllocation


def financial_profile():
    return FinancialProfile(
        monthly_allowance=2200,
        years_to_retirement=25,
    )


def simple_problem() -> UserPersonalFinances:
    return UserPersonalFinances(
        name="simple example",
        financial_profile=financial_profile(),
        portfolio=Portfolio(
            instruments=[
                Loan(
                    name="loan1",
                    apr=5,
                    current_balance=-20000,
                    minimum_monthly_payment=50,
                    final_month=12 * 30,
                ),
                Loan(
                    name="loan2",
                    apr=20,
                    current_balance=-10000,
                    minimum_monthly_payment=50,
                    final_month=12 * 30,
                ),
                Loan(
                    name="loan3",
                    apr=4,
                    current_balance=-200000,
                    minimum_monthly_payment=50,
                    final_month=12 * 30,
                ),
                Investment(
                    name="inv1",
                    apr=5,
                    current_balance=0,
                    minimum_monthly_payment=0,
                    final_month=12 * 30,
                ),
            ]
        ),
    )


def simple_model_input():
    return ProblemInput(
        problem=simple_problem(),
        strategies=["snowball", "avalanche", "avalanche-ball", "linear-program"],
    )


def bad_snowball_problem_input():
    return UserPersonalFinances(
        financial_profile=financial_profile(),
        portfolio=Portfolio(
            loans=[
                Loan(
                    name="credit card",
                    apr=19,
                    current_balance=10000,
                    minimum_monthly_payment=50,
                ),
                Loan(
                    name="car loan",
                    apr=3,
                    current_balance=9000,
                    minimum_monthly_payment=50,
                ),
                Loan(
                    name="loan3",
                    apr=4.5,
                    current_balance=15000,
                    minimum_monthly_payment=50,
                ),
            ]
        ),
    )


def bad_avalanche_problem_input() -> UserPersonalFinances:
    return UserPersonalFinances(
        financial_profile=financial_profile(),
        portfolio=Portfolio(
            loans=[
                Loan(
                    name="loan1",
                    apr=30,
                    current_balance=-15_000,
                    minimum_monthly_payment=0,
                ),
                Loan(
                    name="loan2",
                    apr=31,
                    current_balance=-1000,
                    minimum_monthly_payment=0,
                ),
            ]
        ),
    )


def simple_monthly_allocation() -> MonthlyAllocation:
    return MonthlyAllocation(
        payments={"loan1": 500, "loan2": 500, "loan3": 600},
    )


def final_payment_example() -> Tuple[Portfolio, MonthlyAllocation]:
    portfolio = Portfolio(
        instruments=[
            Loan(
                name="loan",
                apr=5,
                current_balance=-200,
                minimum_monthly_payment=100,
                final_month=10,
            )
        ]
    )
    ma = MonthlyAllocation(payments={"loan": 300})
    return portfolio, ma


def simple_pennies_request() -> PenniesRequest:
    smi = simple_model_input()
    fp = financial_profile()
    return PenniesRequest(
        financial_profile=fp,
        loans=[loan for loan in smi.problem.portfolio.loans],
        investments=[inv for inv in smi.problem.portfolio.investments()],
        strategies=smi.strategies,
    )


def pennies_request_as_dict() -> Dict:
    return simple_pennies_request().dict()
