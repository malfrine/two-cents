import math

from pydantic import validator, root_validator

from pennies.errors.validation_errors import BadDomainException
from pennies.model.instrument import Instrument


class Loan(Instrument):
    @validator("current_balance")
    def validate_non_positive_float(cls, v):
        if v > 0:
            raise BadDomainException("Loan balance must be negative")
        return v

    def is_paid_off(self) -> bool:
        return math.isclose(self.current_balance, 0, abs_tol=0.1)

    def get_type(self) -> str:
        return "loan"


class RevolvingLoan(Loan):
    def get_minimum_monthly_payment(self, month: int):
        return abs(self.current_balance) * self.monthly_interest_rate(month)

    @validator("final_month")
    def validate_no_final_month(cls, v):
        if v is not None:
            raise ValueError("Revolving Loans don't have a final month")
        return v


class InstalmentLoan(Loan):

    minimum_monthly_payment: float

    def get_minimum_monthly_payment(self, month: int):
        return self.minimum_monthly_payment

    @validator("final_month")
    def validate_final_month_not_none(cls, v):
        if v is None:
            raise ValueError("Instalment Loans must have a final month")
        return v


class CarLoan(InstalmentLoan):
    pass


class StudentLoan(InstalmentLoan):
    pass


class StudentLineOfCredit(RevolvingLoan):
    pass


class LineOfCredit(RevolvingLoan):
    pass


class CreditCardLoan(RevolvingLoan):
    pass


class PersonalLoan(InstalmentLoan):
    pass
