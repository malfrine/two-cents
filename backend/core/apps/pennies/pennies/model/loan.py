import math

from pydantic import validator, root_validator

from pennies.errors.validation_errors import BadDomainException
from pennies.model.instrument import Instrument
from pennies.model.interest_rate import InterestRate
from pennies.utilities.finance import LoanMinimumPaymentCalculator


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

    @root_validator
    def validate_minimum_monthly_payment(cls, values):
        principal: float = abs(values["current_balance"])
        interest_rate: InterestRate = values["interest_rate"]
        effective_apr = interest_rate.get_monthly_interest_rate(0) * 12 * 100
        final_month: int = values[
            "final_month"
        ]  # have already validated that final_month is not None
        mmp_lb = LoanMinimumPaymentCalculator.calculate_for_instalment_loan(
            principal, effective_apr, final_month
        )
        mmp = values["minimum_monthly_payment"]
        if mmp_lb > 10 and mmp < mmp_lb:
            raise ValueError(
                f"Loan minimum monthly payment ({mmp}) must be greater than {mmp_lb}"
            )
        else:
            return values


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
