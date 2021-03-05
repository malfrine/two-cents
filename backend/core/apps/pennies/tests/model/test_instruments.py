from pydantic import ValidationError

from pennies.model.instrument import Instrument
from pennies.model.interest_rate import FixedLoanInterestRate, GuaranteedInvestmentReturnRate
from pennies.model.investment import GuaranteedInvestment
from pennies.model.loan import Loan


def test_generic_instrument():
    instrument = Instrument(
        name="generic",
        interest_rate=FixedLoanInterestRate(apr=5),
        current_balance=200,
        minimum_monthly_payment=100,
        final_month=10,
    )
    assert isinstance(instrument, Instrument)


def test_generic_loan():
    loan = Loan(
        name="generic",
        interest_rate=FixedLoanInterestRate(apr=5),
        current_balance=-200,
        minimum_monthly_payment=100,
        final_month=10,
    )
    assert isinstance(loan, Loan)


def test_bad_loan():
    try:
        Loan(
            name="generic",
            interest_rate=FixedLoanInterestRate(apr=5),
            current_balance=200,
            minimum_monthly_payment=100,
            final_month=10,
        )
        assert False
    except Exception as e:
        if isinstance(e, ValidationError):
            assert True
        else:
            assert False


def test_guaranteed_investment():
    principal = 100
    apr = 12
    interest_rate = GuaranteedInvestmentReturnRate(
        interest_rate=FixedLoanInterestRate(apr=apr),
        final_month=1
    )
    gi = GuaranteedInvestment(
        name="generic",
        principal_investment_amount=principal,
        start_month=-1,
        final_month=1,
        interest_rate=interest_rate,
        current_balance=None,
    )
    assert gi.current_balance == principal * (1 + apr / 100 / 12)
