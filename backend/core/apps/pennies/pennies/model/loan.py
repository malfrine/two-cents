import math

from pydantic import validator
from pydantic.main import BaseModel

from pennies.errors.validation_errors import BadDomainException
from pennies.model.instrument import Instrument


class Loan(Instrument):
    @validator("current_balance")
    def validate_non_positive_float(cls, v):
        if v > 0:
            raise BadDomainException("Loan balance must be negative")
        return v

    def receive_payment(self, payment: float) -> float:
        payment = min(payment, abs(self.current_balance))  # balance <= 0
        self._add_to_current_balance(payment)
        return payment

    def is_paid_off(self) -> bool:
        return math.isclose(self.current_balance, 0)

    def get_type(self) -> str:
        return "loan"
