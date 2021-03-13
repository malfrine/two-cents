from typing import Tuple

import pytest

from pennies.model.interest_rate import (
    FixedLoanInterestRate,
    GuaranteedInvestmentReturnRate,
)
from pennies.model.investment import GuaranteedInvestment
from pennies.model.loan import PersonalLoan
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import MonthlyAllocation
from pennies.utilities.examples import (
    simple_user_finances,
)

TEST_MONTH = 0


def simple_monthly_allocation() -> MonthlyAllocation:
    return MonthlyAllocation(
        payments={"loan1": 500, "loan2": 500, "loan3": 600},
    )


def final_payment_example() -> Tuple[Portfolio, MonthlyAllocation]:
    portfolio = Portfolio(
        instruments=[
            PersonalLoan(
                name="loan",
                interest_rate=FixedLoanInterestRate(apr=5),
                current_balance=-200,
                minimum_monthly_payment=100,
                final_month=10,
            )
        ]
    )
    ma = MonthlyAllocation(payments={"loan": 300})
    return portfolio, ma


def _forward(
    portfolio: Portfolio, ma: MonthlyAllocation
) -> Tuple[Portfolio, Portfolio]:
    before = portfolio
    after = PortfolioManager.forward_on_month(before, ma.payments, TEST_MONTH)
    return before, after


def test_forward_on_month():
    ma = simple_monthly_allocation()
    before, after = _forward(simple_user_finances().portfolio, ma)
    for after_loan in after.loans:
        pytest.approx(
            after_loan.current_balance,
            (
                before.get_loan(after_loan.id_).current_balance
                * (1 + after_loan.monthly_interest_rate(TEST_MONTH))
                + ma[after_loan.id_]
            ),
        )


def test_final_payment():
    portfolio, ma = final_payment_example()
    before, after = _forward(portfolio, ma)
    loan_name = "loan"
    assert loan_name not in after.loans


def test_forward_on_guaranteed_investment():
    principal = 100
    apr = 12
    interest_rate = GuaranteedInvestmentReturnRate(
        interest_rate=FixedLoanInterestRate(apr=apr), final_month=1
    )
    gi = GuaranteedInvestment(
        name="generic",
        principal_investment_amount=principal,
        start_month=-1,
        final_month=1,
        interest_rate=interest_rate,
        current_balance=None,
    )
    p = Portfolio(instruments={gi.id_: gi})
    p = PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=0)
    nb = gi.current_balance * (1 + gi.monthly_interest_rate(0))
    assert p.instruments["generic"].current_balance == nb
    p = PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=1)
    nb = nb * (1 + gi.monthly_interest_rate(1))
    assert p.instruments["generic"].current_balance == nb
    p = PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=2)
    assert p.instruments["generic"].current_balance == nb
    p = PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=3)
    assert p.instruments["generic"].current_balance == nb
