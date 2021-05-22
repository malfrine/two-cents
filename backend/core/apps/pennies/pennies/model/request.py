from enum import Enum
from typing import List, Optional

from pydantic import root_validator, validator
from pydantic.main import BaseModel

from pennies.model.constants import InvestmentAccountType
from pennies.model.financial_profile import FinancialProfile
from pennies.model.goal import AllGoalTypes
from pennies.model.loan import Loan, AllLoanTypes


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
    minimum_monthly_payment: Optional[float] = None
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


class RequestInvestmentType(Enum):
    MUTUAL_FUND = "Mutual Fund"
    ETF = "ETF"
    GIC = "GIC"
    TERM_DEPOSIT = "Term Deposit"
    STOCK = "Stock"
    # BOND = "Bond"
    CASH = "Cash"


class RequestInvestment(BaseModel):
    name: str
    investment_type: RequestInvestmentType = RequestInvestmentType.MUTUAL_FUND
    account_type: InvestmentAccountType
    roi: Optional[float] = None
    volatility: Optional[float] = None
    current_balance: Optional[float] = None
    prime_modifier: Optional[float] = None
    pre_authorized_monthly_contribution: float = 0
    principal_investment_amount: Optional[float] = None
    start_month: Optional[int] = None
    final_month: Optional[int] = None
    interest_type: Optional[InterestType] = None

    @validator("account_type")
    def parse_account_type(cls, v):
        if not isinstance(v, InvestmentAccountType):
            return InvestmentAccountType[str(v)]
        else:
            return v


class PenniesRequest(BaseModel):
    financial_profile: FinancialProfile
    loans: List[AllLoanTypes]
    goals: List[AllGoalTypes]
    investments: List[RequestInvestment]
    strategies: List[str]

    @root_validator
    def validate_instruments_exist(cls, values):
        if not (values["loans"] or values["investments"]):
            raise ValueError("No loans or investments exist")
        return values
