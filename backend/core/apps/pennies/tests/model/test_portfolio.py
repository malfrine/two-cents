from typing import Tuple

import pytest

from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import MonthlyAllocation
from tests.examples import (
    simple_monthly_allocation,
    simple_problem,
    final_payment_example,
)


def _forward(
    portfolio: Portfolio, ma: MonthlyAllocation
) -> Tuple[Portfolio, Portfolio]:
    before = portfolio
    after: Portfolio = portfolio.copy(deep=True)
    PortfolioManager.forward_on_month(after, ma.payments)
    return before, after


def test_forward_on_month():
    ma = simple_monthly_allocation()
    before, after = _forward(simple_problem().portfolio, ma)
    for after_loan in after.loans:
        pytest.approx(
            after_loan.current_balance,
            (
                before.get_loan(after_loan.name).current_balance
                * (1 + after_loan.monthly_interest_rate)
                + ma[after_loan.name]
            ),
        )


def test_final_payment():
    portfolio, ma = final_payment_example()
    before, after = _forward(portfolio, ma)
    loan_name = "loan"
    assert loan_name not in after.loans
