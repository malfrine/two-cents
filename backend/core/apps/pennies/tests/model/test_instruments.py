from pydantic import ValidationError

from pennies.model.instrument import Instrument
from pennies.model.interest_rate import FixedInterestRate
from pennies.model.loan import Loan


def test_generic_instrument():
    instrument = Instrument(
        name="generic",
        interest_rate=FixedInterestRate(apr=5),
        current_balance=200,
        minimum_monthly_payment=100,
        final_month=10,
    )
    assert isinstance(instrument, Instrument)


def test_generic_loan():
    loan = Loan(
        name="generic",
        interest_rate=FixedInterestRate(apr=5),
        current_balance=-200,
        minimum_monthly_payment=100,
        final_month=10,
    )
    assert isinstance(loan, Loan)


def test_bad_loan():
    try:
        Loan(
            name="generic",
            interest_rate=FixedInterestRate(apr=5),
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
