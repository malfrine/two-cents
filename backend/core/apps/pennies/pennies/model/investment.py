from pydantic import validator

from pennies.errors.validation_errors import BadDomainException
from pennies.model.instrument import Instrument
from pennies.utilities.datetime import MONTHS_IN_YEAR


class Investment(Instrument):

    minimum_monthly_payment: float
    volatility: float  # the volatility is defined as the standard deviation of the roi

    def get_minimum_monthly_payment(self, month: int):
        return self.minimum_monthly_payment

    @validator("current_balance")
    def validate_negative_balance(cls, v):
        if v < 0:
            raise BadDomainException("Investment balance must be positive")
        return v

    @property
    def volatility_fraction(self):
        return self.volatility / 100 / MONTHS_IN_YEAR

    def withdraw(self, amount: float):
        amount = min(amount, self.current_balance)
        self._reduce_current_balance(amount)

    def receive_payment(self, payment) -> float:
        self._add_to_current_balance(payment)
        return payment

    def get_type(self) -> str:
        return "investment"
