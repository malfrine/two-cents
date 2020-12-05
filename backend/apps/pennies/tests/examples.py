from typing import Tuple, Dict

from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.model_input import ModelInput
from pennies.model.portfolio import Portfolio
from pennies.model.problem import Problem
from pennies.model.request import PenniesRequest
from pennies.model.solution import MonthlyAllocation


def simple_problem() -> Problem:
    return Problem(
        name="simple example",
        monthly_allowance=2100,
        portfolio=Portfolio(
            instruments=[
                Loan(
                    name="loan1",
                    annual_interest_rate=0.05,
                    current_balance=-20000,
                    minimum_monthly_payment=50,
                    final_month=12 * 30
                ),
                Loan(
                    name="loan2",
                    annual_interest_rate=0.20,
                    current_balance=-10000,
                    minimum_monthly_payment=50,
                    final_month=12 * 30
                ),
                Loan(
                    name="loan3",
                    annual_interest_rate=0.04,
                    current_balance=-200000,
                    minimum_monthly_payment=50,
                    final_month=12 * 30
                ),
                Investment(
                    name="inv1",
                    annual_interest_rate=0.05,
                    current_balance=0,
                    minimum_monthly_payment=0,
                    final_month=12 * 30
                )
            ]
        )
    )

def simple_model_input():
    return ModelInput(
        problem=simple_problem(),
        strategies=["snowball", "avalanche", "avalanche-ball", "linear-program"]
    )

def bad_snowball_problem_input():
    return Problem(
        monthly_allowance=420,
        portfolio=Portfolio(
            loans=[
                Loan(
                    name="credit card",
                    annual_interest_rate=0.19,
                    current_balance=10000,
                    minimum_monthly_payment=50
                ),
                Loan(
                    name="car loan",
                    annual_interest_rate=0.03,
                    current_balance=9000,
                    minimum_monthly_payment=50
                ),
                Loan(
                    name="loan3",
                    annual_interest_rate=0.045,
                    current_balance=15000,
                    minimum_monthly_payment=50
                )
            ]
        )
    )


def bad_avalanche_problem_input() -> Problem:
    return Problem(
        monthly_allowance=430,
        portfolio=Portfolio(
            loans=[
                Loan(
                    name="loan1",
                    annual_interest_rate=0.30,
                    current_balance=-15_000,
                    minimum_monthly_payment=0
                ),
                Loan(
                    name="loan2",
                    annual_interest_rate=0.31,
                    current_balance=-1000,
                    minimum_monthly_payment=0
                )
            ]
        )
    )


def simple_monthly_allocation() -> MonthlyAllocation:
    return MonthlyAllocation(
        payments={"loan1": 500, "loan2": 500, "loan3": 600},
    )

def final_payment_example() -> Tuple[Portfolio, MonthlyAllocation]:
    portfolio = Portfolio(
        instruments=[Loan(
            name="loan",
            annual_interest_rate=0.05,
            current_balance=-200,
            minimum_monthly_payment=100,
            final_month=10
        )]
    )
    ma = MonthlyAllocation(
        payments={"loan": 300}
    )
    return portfolio, ma

def simple_pennies_request() -> PenniesRequest:
    smi = simple_model_input()
    return PenniesRequest(
        monthly_allowance=smi.problem.monthly_allowance,
        loans=[loan for loan in smi.problem.portfolio.loans],
        investments=[inv for inv in smi.problem.portfolio.investments()],
        strategies=smi.strategies
    )

def pennies_request_as_dict() -> Dict:
    return simple_pennies_request().dict()
