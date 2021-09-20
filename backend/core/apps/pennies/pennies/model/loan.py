import math
from typing import Any, Literal, Union, Optional

from pydantic import validator

from pennies.model.instrument import Instrument
from pennies.model.interest_rate import AllLoanInterestTypes

MIN_REVOLVING_LOAN_PAYMENT_THRESHOLD = 10  # dollars


class Loan(Instrument):

    loan_type: Any
    interest_rate: AllLoanInterestTypes

    @validator("current_balance")
    def validate_non_positive_float(cls, v):
        if v > 0:
            return 0
        return v

    def is_paid_off(self) -> bool:
        return math.isclose(self.current_balance, 0, abs_tol=0.1)

    def get_type(self) -> str:
        return "loan"


class RevolvingLoan(Loan):
    def get_minimum_monthly_payment(self, month: int):
        min_payment = abs(self.current_balance) * self.monthly_interest_rate(month)
        return min_payment if min_payment > MIN_REVOLVING_LOAN_PAYMENT_THRESHOLD else 0

    @validator("final_month")
    def validate_no_final_month(cls, v):
        return None


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
    loan_type: Literal["Car Loan"] = "Car Loan"


class StudentLoan(InstalmentLoan):
    loan_type: Literal["Student Loan"] = "Student Loan"


class StudentLineOfCredit(RevolvingLoan):
    loan_type: Literal["Student Line of Credit"] = "Student Line of Credit"


class LineOfCredit(RevolvingLoan):
    loan_type: Literal["Line of Credit"] = "Line of Credit"


class CreditCard(RevolvingLoan):
    loan_type: Literal["Credit Card"] = "Credit Card"


class PersonalLoan(InstalmentLoan):
    loan_type: Literal["Personal Loan"] = "Personal Loan"


class Mortgage(Loan):
    loan_type: Literal["Mortgage"] = "Mortgage"

    minimum_monthly_payment: float

    def get_minimum_monthly_payment(self, month: int):
        return self.minimum_monthly_payment

    def get_maximum_monthly_payment(self, month: int) -> Optional[float]:
        return self.minimum_monthly_payment


AllLoanTypes = Union[
    CarLoan,
    StudentLoan,
    StudentLineOfCredit,
    LineOfCredit,
    CreditCard,
    PersonalLoan,
    Mortgage,
]
