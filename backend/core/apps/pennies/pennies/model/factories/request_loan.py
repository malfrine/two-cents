from typing import Optional

from pennies.model.interest_rate import (
    FixedLoanInterestRate,
    VariableLoanInterestRate,
)
from pennies.model.prime import CURRENT_PRIME
from pennies.model.request import RequestLoanType, RequestLoan, InterestType
from pennies.utilities.finance import LoanMinimumPaymentCalculator


class RequestLoanFactory:
    """Primarily just used for test examples"""

    INSTALMENT_LOANS = {
        RequestLoanType.PERSONAL_LOAN,
        RequestLoanType.CAR_LOAN,
        RequestLoanType.STUDENT_LOAN,
    }

    REVOLVING_LOANS = {
        RequestLoanType.LINE_OF_CREDIT,
        RequestLoanType.STUDENT_LINE_OF_CREDIT,
        RequestLoanType.CREDIT_CARD,
    }

    @classmethod
    def create(
        cls,
        name: str,
        current_balance: float,
        loan_type: RequestLoanType,
        interest_type: InterestType,
        final_month: Optional[int] = None,
        apr: Optional[float] = None,
        prime_modifier: Optional[float] = None,
    ):
        interest_rate = (
            prime_modifier + CURRENT_PRIME
            if interest_type == InterestType.VARIABLE
            else apr
        )
        mmp = None
        if loan_type in cls.INSTALMENT_LOANS:
            if final_month is None:
                raise ValueError(
                    f"{loan_type} is an instalment loan and requires a final_month"
                )
            mmp = LoanMinimumPaymentCalculator.calculate_for_instalment_loan(
                abs(current_balance), interest_rate, final_month
            )
        return RequestLoan(
            name=name,
            apr=apr,
            prime_modifier=prime_modifier,
            current_balance=current_balance,
            final_month=final_month,
            minimum_monthly_payment=mmp,
            loan_type=loan_type,
            interest_type=interest_type,
        )
