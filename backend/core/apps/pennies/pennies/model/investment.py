from pydantic import validator

from pennies.errors.validation_errors import BadDomainException
from pennies.model.instrument import Instrument


class Investment(Instrument):
    ...

    @validator("current_balance")
    def validate_negative_balance(cls, v):
        if v < 0:
            raise BadDomainException("Investment balance must be positive")
        return v

    def withdraw(self, amount: float):
        amount = min(amount, self.current_balance)
        self._reduce_current_balance(amount)

    def receive_payment(self, payment) -> float:
        self._add_to_current_balance(payment)
        return payment

    def get_type(self) -> str:
        return "investment"
