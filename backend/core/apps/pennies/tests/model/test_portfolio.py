from typing import Tuple, Dict
from uuid import UUID

import pytest

from pennies.model.constants import Province
from pennies.model.financial_profile import FinancialProfile
from pennies.model.interest_rate import (
    FixedLoanInterestRate,
    GuaranteedInvestmentReturnRate,
    FixedInvestmentInterestRate,
)
from pennies.model.investment import GuaranteedInvestment
from pennies.model.loan import PersonalLoan, LineOfCredit, StudentLineOfCredit
from pennies.model.portfolio import Portfolio
from pennies.model.portfolio_manager import PortfolioManager
from pennies.model.solution import MonthlyAllocation
from pennies.model.user_personal_finances import UserPersonalFinances

TEST_MONTH = 0


def final_payment_example() -> Tuple[Portfolio, MonthlyAllocation]:
    loans = [
        PersonalLoan(
            name="loan",
            interest_rate=FixedLoanInterestRate(apr=5),
            current_balance=-200,
            minimum_monthly_payment=100,
            final_month=10,
        )
    ]
    portfolio = Portfolio(instruments={loan.id_: loan for loan in loans})
    name_to_id = {loan.name: loan.id_ for loan in loans}
    ma = MonthlyAllocation(payments={name_to_id["loan"]: 300})
    return portfolio, ma


def _forward(
    portfolio: Portfolio, ma: MonthlyAllocation
) -> Tuple[Portfolio, Portfolio]:
    before = portfolio
    after = portfolio.copy(deep=True)
    PortfolioManager.forward_on_month(after, ma.payments, TEST_MONTH)
    return before, after


def make_user_finances() -> UserPersonalFinances:
    loans = [
        PersonalLoan(
            name="loan1",
            interest_rate=FixedLoanInterestRate(apr=3.5),
            current_balance=-20000,
            final_month=12 * 10,
            minimum_monthly_payment=50,
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
        ),
    ]

    financial_profile = FinancialProfile(
        years_to_retirement=40,
        risk_tolerance=0,
        province_of_residence=Province.AB,
        starting_rrsp_contribution_limit=0,
        starting_tfsa_contribution_limit=0,
        current_age=25,
        monthly_salary_before_tax=5000,
        percent_salary_for_spending=50,
        years_to_death=65,
    )

    return UserPersonalFinances(
        portfolio=Portfolio(instruments={loan.id_: loan for loan in loans}),
        financial_profile=financial_profile,
        goals=dict(),
    )


def simple_monthly_allocation(name_to_id: Dict[str, UUID]) -> MonthlyAllocation:
    return MonthlyAllocation(
        payments={
            name_to_id["loan1"]: 500,
            name_to_id["loan2"]: 500,
            name_to_id["loan3"]: 600,
        }
    )


def test_forward_on_month():
    user_finances = make_user_finances()
    name_to_id = {l.name: l.id_ for l in user_finances.portfolio.loans}
    ma = simple_monthly_allocation(name_to_id)
    before, after = _forward(user_finances.portfolio, ma)
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
    roi = 12
    interest_rate = GuaranteedInvestmentReturnRate(
        interest_rate=FixedInvestmentInterestRate(roi=roi), final_month=1
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
    PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=0)
    nb = gi.current_balance * (1 + gi.monthly_interest_rate(0))
    assert p.instruments[gi.id_].current_balance == nb
    PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=1)
    nb = nb * (1 + gi.monthly_interest_rate(1))
    assert p.instruments[gi.id_].current_balance == nb
    PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=2)
    assert p.instruments[gi.id_].current_balance == nb
    PortfolioManager.forward_on_month(portfolio=p, payments=dict(), month=3)
    assert p.instruments[gi.id_].current_balance == nb
