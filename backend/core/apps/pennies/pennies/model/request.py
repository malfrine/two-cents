from enum import Enum
from typing import List, Optional

from pydantic import root_validator
from pydantic.main import BaseModel

from pennies.model.financial_profile import FinancialProfile
from pennies.model.loan import Loan


class RequestLoanType(Enum):
    CREDIT_CARD = "Credit Card"
    LINE_OF_CREDIT = "Line of Credit"
    STUDENT_LOAN = "Student Loan"
    STUDENT_LINE_OF_CREDIT = "Student Line of Credit"
    PERSONAL_LOAN = "Personal Loan"
    CAR_LOAN = "Car Loan"


class InterestType(Enum):
    FIXED = "Fixed"
    VARIABLE = "Variable"


class RequestLoan(BaseModel):
    name: str
    current_balance: float
    minimum_monthly_payment: float
    apr: Optional[float] = None
    prime_modifier: Optional[float] = None
    final_month: int = None
    loan_type: RequestLoanType = RequestLoanType.PERSONAL_LOAN
    interest_type: InterestType = InterestType.FIXED

    @root_validator
    def validate_apr_or_prime_modifier(cls, values):
        interest_type = values["interest_type"]
        if interest_type == InterestType.FIXED and values["apr"] is None:
            raise ValueError("Fixed interest loans must have an APR")
        elif (
            interest_type == InterestType.VARIABLE and values["prime_modifier"] is None
        ):
            raise ValueError("Variable interest loans must have an APR")
        return values


class RequestInvestment(BaseModel):
    name: str
    apr: float
    current_balance: float
    minimum_monthly_payment: float
    final_month: int = None


class PenniesRequest(BaseModel):
    financial_profile: FinancialProfile
    loans: List[RequestLoan]
    investments: List[RequestInvestment]
    strategies: List[str]

    @root_validator
    def validate_instruments_exist(cls, values):
        if not (values["loans"] or values["investments"]):
            raise ValueError("No loans or investments exist")
        return values

    @root_validator
    def validate_enough_monthly_allowance(cls, values):
        loans: List[Loan] = values["loans"]
        total_min_payments = sum(l.minimum_monthly_payment for l in loans)
        financial_profile: FinancialProfile = values["financial_profile"]
        if total_min_payments >= financial_profile.monthly_allowance:
            raise ValueError(
                f"Total minimum loan payments ({total_min_payments} "
                f"is greater than or equal to monthly allowance {financial_profile.monthly_allowance}"
            )
        return values


