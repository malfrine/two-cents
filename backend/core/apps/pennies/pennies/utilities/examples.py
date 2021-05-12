from typing import Tuple, Dict, List, ClassVar

from pennies.model.constants import Province, InvestmentAccountType
from pennies.model.factories.problem_input import ProblemInputFactory
from pennies.model.factories.request_loan import RequestLoanFactory
from pennies.model.financial_profile import FinancialProfile
from pennies.model.interest_rate import FixedLoanInterestRate, VariableLoanInterestRate, InterestRate
from pennies.model.loan import Loan, PersonalLoan, LineOfCredit, StudentLineOfCredit, StudentLoan, CreditCard
from pennies.model.portfolio import Portfolio
from pennies.model.problem_input import ProblemInput
from pennies.model.request import (
    PenniesRequest,
    RequestInvestment,
    InterestType,
    RequestInvestmentType,
)
from pennies.model.solution import MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies import StrategyName


def financial_profile():
    return FinancialProfile(
        years_to_retirement=40,
        risk_tolerance=50,
        province_of_residence=Province.AB,
        starting_rrsp_contribution_limit=0,
        starting_tfsa_contribution_limit=0,
        current_age=25,
        monthly_salary_before_tax=5000,
        percent_salary_for_spending=25,
        years_to_death=65
    )


def simple_request_loans() -> List[Loan]:
    return [
        PersonalLoan(
            name="loan1",
            interest_rate=FixedLoanInterestRate(apr=3.5),
            current_balance=-20000,
            final_month=12 * 10,
            minimum_monthly_payment=50
        ),
        LineOfCredit(
            name="loan2",
            interest_rate=FixedLoanInterestRate(apr=4.1),
            current_balance=-10000,
        ),
        StudentLineOfCredit(
            name="loan3",
            interest_rate=FixedLoanInterestRate(apr=3.5),
            current_balance=-200000,
        )
    ]


def all_possible_loans() -> List[Loan]:
    default_apr = 1
    default_prime_modifier = -2
    default_current_balance = -10

    def make_loan(loan_class: ClassVar[Loan], interest_class: ClassVar[InterestRate]) -> Loan:
        interest_rate = interest_class(
            apr=default_apr,
            prime_modifier=default_prime_modifier
        )
        loan = loan_class(
            name=f"{loan_class.__name__}-{interest_class.__name__}",
            interest_rate=interest_rate,
            current_balance=default_current_balance,
            final_month=10,
            minimum_monthly_payment=0
        )
        return loan

    return [
        make_loan(loan_class, interest_class)
        for loan_class in [CreditCard, StudentLoan]
        for interest_class in [FixedLoanInterestRate, VariableLoanInterestRate]
    ]


def simple_investments() -> List[RequestInvestment]:
    return [
        RequestInvestment(
            name="medium risk (non-registered)",
            roi=5.0,
            current_balance=0,
            pre_authorized_monthly_contribution=0,
            volatility=5.0,
            investment_type=RequestInvestmentType.MUTUAL_FUND,
            account_type=InvestmentAccountType.NON_REGISTERED
        ),
        RequestInvestment(
            name="low risk (rrsp)",
            roi=3.0,
            current_balance=0,
            pre_authorized_monthly_contribution=0,
            volatility=1.0,
            investment_type=RequestInvestmentType.MUTUAL_FUND,
            account_type=InvestmentAccountType.RRSP
        ),
        RequestInvestment(
            name="medium risk (tfsa)",
            roi=5.0,
            current_balance=0,
            pre_authorized_monthly_contribution=0,
            volatility=5.0,
            investment_type=RequestInvestmentType.MUTUAL_FUND,
            account_type=InvestmentAccountType.TFSA
        ),
        # RequestInvestment(
        #     name="term deposit",
        #     investment_type=RequestInvestmentType.TERM_DEPOSIT,
        #     final_month=100,
        #     principal_investment_amount=100000,
        #     start_month=-36,
        #     interest_type=InterestType.VARIABLE,
        #     prime_modifier=0,
        #     volatility=0,
        #     account_type=RequestInvestmentAccountType.NON_REGISTERED
        # ),
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
            account_type=InvestmentAccountType.TFSA
        ),
        RequestInvestment(
            name="etf",
            current_balance=0,
            investment_type=RequestInvestmentType.ETF,
            roi=5,
            volatility=5,
            pre_authorized_monthly_contribution=0,
            account_type=InvestmentAccountType.RRSP
        ),
        RequestInvestment(
            name="stock",
            current_balance=0,
            investment_type=RequestInvestmentType.STOCK,
            roi=5,
            volatility=5,
            pre_authorized_monthly_contribution=0,
            account_type=InvestmentAccountType.NON_REGISTERED,
        ),
        RequestInvestment(
            name="cash",
            current_balance=0,
            investment_type=RequestInvestmentType.CASH,
            pre_authorized_monthly_contribution=10,
            account_type=InvestmentAccountType.NON_REGISTERED
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
            account_type=InvestmentAccountType.TFSA
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
            account_type=InvestmentAccountType.NON_REGISTERED
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
