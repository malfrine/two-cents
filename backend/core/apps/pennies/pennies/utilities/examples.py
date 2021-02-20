from typing import Tuple, Dict, List

from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.factories.request_loan import RequestLoanFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.interest_rate import FixedLoanInterestRate
from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.portfolio import Portfolio
from pennies.model.problem_input import ProblemInput
from pennies.model.request import (
    PenniesRequest,
    RequestLoan,
    RequestLoanType,
    RequestInvestment,
    InterestType,
    RequestInvestmentType,
)
from pennies.model.solution import MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies import StrategyName


def financial_profile():
    return FinancialProfile(
        monthly_allowance=2500,
        years_to_retirement=35,
    )


def simple_request_loans() -> List[RequestLoan]:
    return [
        RequestLoanFactory.create(
            name="loan1",
            apr=5,
            current_balance=-20000,
            loan_type=RequestLoanType.PERSONAL_LOAN,
            final_month=12 * 10,
            interest_type=InterestType.FIXED,
        ),
        RequestLoanFactory.create(
            name="loan2",
            apr=20,
            current_balance=-10000,
            loan_type=RequestLoanType.LINE_OF_CREDIT,
            interest_type=InterestType.FIXED,
        ),
        RequestLoanFactory.create(
            name="loan3",
            apr=3.5,
            current_balance=-200000,
            loan_type=RequestLoanType.STUDENT_LINE_OF_CREDIT,
            interest_type=InterestType.FIXED,
        ),
    ]


def all_possible_loans() -> List[RequestLoan]:
    default_apr = 1
    default_prime_modifier = -2
    default_current_balance = -10

    return [
        RequestLoanFactory.create(
            name=f"{loan_type.value}-{interest_type.value}",
            apr=default_apr if interest_type == InterestType.FIXED else None,
            prime_modifier=default_prime_modifier
            if interest_type == InterestType.VARIABLE
            else None,
            current_balance=default_current_balance,
            loan_type=loan_type,
            final_month=10
            if loan_type in RequestLoanFactory.INSTALMENT_LOANS
            else None,
            interest_type=interest_type,
        )
        for loan_type in RequestLoanType
        for interest_type in InterestType
    ]


def simple_investments() -> List[RequestInvestment]:
    return [
        RequestInvestment(
            name="high risk",
            roi=7,
            current_balance=0,
            minimum_monthly_payment=0,
            volatility=10,
            investment_type=RequestInvestmentType.MUTUAL_FUND,
        ),
        RequestInvestment(
            name="low risk",
            roi=4,
            current_balance=0,
            minimum_monthly_payment=0,
            volatility=2.5,
            investment_type=RequestInvestmentType.MUTUAL_FUND,
        ),
        RequestInvestment(
            name="medium risk",
            roi=5.5,
            current_balance=0,
            minimum_monthly_payment=0,
            volatility=5.5,
            investment_type=RequestInvestmentType.MUTUAL_FUND,
        ),
        RequestInvestment(
            name="term deposit",
            investment_type=RequestInvestmentType.TERM_DEPOSIT,
            final_month=36,
            principal_investment_amount=100000,
            start_month=-36,
            interest_type=InterestType.VARIABLE,
            prime_modifier=0,
            volatility=0,
        ),
    ]


def all_possible_investments() -> List[RequestInvestment]:
    return [
        RequestInvestment(
            name="mutual fund",
            current_balance=0,
            investment_type=RequestInvestmentType.MUTUAL_FUND,
            roi=5,
            volatility=5,
            pre_authorized_monthly_contribution=0,
        ),
        RequestInvestment(
            name="etf",
            current_balance=0,
            investment_type=RequestInvestmentType.ETF,
            roi=5,
            volatility=5,
            pre_authorized_monthly_contribution=0,
        ),
        RequestInvestment(
            name="stock",
            current_balance=0,
            investment_type=RequestInvestmentType.STOCK,
            roi=5,
            volatility=5,
            pre_authorized_monthly_contribution=0,
        ),
        RequestInvestment(
            name="cash",
            current_balance=0,
            investment_type=RequestInvestmentType.CASH,
            pre_authorized_monthly_contribution=10,
        ),
        RequestInvestment(
            name="gic",
            investment_type=RequestInvestmentType.GIC,
            roi=2,
            final_month=36,
            principal_investment_amount=1000,
            start_month=-36,
            interest_type=InterestType.FIXED,
            volatility=0,
        ),
        RequestInvestment(
            name="term deposit",
            investment_type=RequestInvestmentType.TERM_DEPOSIT,
            final_month=36,
            principal_investment_amount=1000,
            start_month=-36,
            interest_type=InterestType.VARIABLE,
            prime_modifier=0,
            volatility=0,
        ),
    ]


def all_strategies() -> List[str]:
    return [
        StrategyName.snowball.value,
        StrategyName.lp.value,
        StrategyName.avalanche.value,
        StrategyName.avalanche_ball.value,
    ]


def simple_request() -> PenniesRequest:
    return PenniesRequest(
        financial_profile=financial_profile(),
        loans=simple_request_loans(),
        investments=simple_investments(),
        strategies=all_strategies(),
    )


def all_instrument_types_request() -> PenniesRequest:
    return PenniesRequest(
        financial_profile=financial_profile(),
        loans=all_possible_loans(),
        investments=all_possible_investments(),
        strategies=all_strategies(),
    )


def only_investments_request() -> PenniesRequest:
    return PenniesRequest(
        financial_profile=financial_profile(),
        loans=[],
        investments=simple_investments(),
        strategies=all_strategies(),
    )


def simple_user_finances() -> UserPersonalFinances:
    return ProblemInputFactory.from_request(simple_request()).user_finances


def simple_model_input():
    return ProblemInput(
        user_finances=simple_user_finances(),
        strategies=[
            StrategyName.snowball.value,
            StrategyName.avalanche.value,
            StrategyName.avalanche_ball.value,
            StrategyName.lp.value,
        ],
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


def pennies_request_as_dict() -> Dict:
    return simple_request().dict()


def all_requests() -> List[PenniesRequest]:
    return [
        simple_request(),
        all_instrument_types_request(),
        only_investments_request(),
    ]


def all_requests_as_dicts() -> List[Dict]:
    return [req.dict() for req in all_requests()]
