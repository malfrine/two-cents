from pennies.model.interest_rate import (
    FixedLoanInterestRate,
    VariableLoanInterestRate,
)
from pennies.model.loan import (
    Loan,
    PersonalLoan,
    StudentLineOfCredit,
    StudentLoan,
    LineOfCredit,
    CreditCardLoan,
    CarLoan,
)
from pennies.model.request import RequestLoan, RequestLoanType, InterestType


class LoanFactory:

    _LOAN_MAP = {
        RequestLoanType.PERSONAL_LOAN: PersonalLoan,
        RequestLoanType.STUDENT_LOAN: StudentLoan,
        RequestLoanType.STUDENT_LINE_OF_CREDIT: StudentLineOfCredit,
        RequestLoanType.LINE_OF_CREDIT: LineOfCredit,
        RequestLoanType.CREDIT_CARD: CreditCardLoan,
        RequestLoanType.CAR_LOAN: CarLoan,
    }

    _INTEREST_RATE_MAP = {
        InterestType.FIXED: FixedLoanInterestRate,
        InterestType.VARIABLE: VariableLoanInterestRate,
    }

    @classmethod
    def from_request_loan(cls, request_loan: RequestLoan) -> Loan:
        interest_rate = cls._INTEREST_RATE_MAP[request_loan.interest_type].parse_obj(
            request_loan.dict()
        )
        return cls._LOAN_MAP[request_loan.loan_type].parse_obj(
            dict(request_loan.dict(), interest_rate=interest_rate)
        )
