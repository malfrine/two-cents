from pennies import strategies
from pennies.model.constants import InvestmentAccountType
from pennies.model.interest_rate import FixedLoanInterestRate, InvestmentReturnRate
from pennies.model.investment import MutualFund
from pennies.model.loan import (
    LineOfCredit,
    PersonalLoan,
    StudentLineOfCredit,
)
from pennies.model.request import PenniesRequest
from pennies.model.response import PenniesResponse
from pennies.model.status import PenniesStatus
from pennies.main import solve_request
from pennies.utilities.examples import financial_profile


def make_request():
    return PenniesRequest(
        financial_profile=financial_profile(),
        loans=[
            PersonalLoan(
                name="0 APR Personal Loan",
                interest_rate=FixedLoanInterestRate(apr=0),
                current_balance=-20000,
                final_month=12 * 10,
                minimum_monthly_payment=50,
            ),
            LineOfCredit(
                name="4.1 APR LOC",
                interest_rate=FixedLoanInterestRate(apr=4.1),
                current_balance=-10000,
            ),
            StudentLineOfCredit(
                name="3.5 APR Student LOC",
                interest_rate=FixedLoanInterestRate(apr=3.5),
                current_balance=-200000,
            ),
        ],
        investments=[
            MutualFund(
                name="medium risk (rrsp)",
                interest_rate=InvestmentReturnRate(roi=5.0, volatility=5.0),
                current_balance=0,
                pre_authorized_monthly_contribution=0,
                account_type=InvestmentAccountType.RRSP,
            )
        ],
        goals=list(),
        strategies=[
            strategies.StrategyName.two_cents_milp.value,
            strategies.StrategyName.snowball.value,
        ],
    )


def test_single_bad_loan():
    request = make_request()
    response = PenniesResponse.parse_obj(solve_request(request=request.dict()))
    assert isinstance(response, PenniesResponse)
    assert response.status == PenniesStatus.SUCCESS
