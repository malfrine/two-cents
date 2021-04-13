from enum import Enum
from typing import Literal, ClassVar, List, Union, Any

from pydantic import BaseModel

from pennies.model.loan import AllLoanTypes, CarLoan, StudentLoan, Mortgage


def get_data():
    return {
    "loans": [
        {
            "name": "Mortgage",
            "loan_type": "Mortgage",
            "interest_rate": {
                "interest_type": "Interest Rate Terms",
                "terms": [
                    {
                        "interest_rate": {
                            "interest_type": "Fixed",
                            "apr": 2.0
                        },
                        "start_month": -1,
                        "final_month": 11
                    }
                ]
            },
            "start_month": -11,
            "final_month": 1,
            "monthly_payment": 1.0,
            "purchase_price": 10.0,
            "downpayment_amount": 1.0
        },
        {
            "interest_rate": {
                "interest_type": "Fixed",
                "apr": 4.1
            },
            "current_balance": -10000.0,
            "final_month": 108,
            "name": "Student Loan",
            "loan_type": "Student Loan",
            "minimum_monthly_payment": 111.0
        },
        {
            "name": "House",
            "loan_type": "Mortgage",
            "interest_rate": {
                "interest_type": "Interest Rate Terms",
                "terms": [
                    {
                        "interest_rate": {
                            "interest_type": "Fixed",
                            "apr": 3.0
                        },
                        "start_month": -1,
                        "final_month": 119
                    }
                ]
            },
            "start_month": -1,
            "final_month": 323,
            "monthly_payment": 1200.0,
            "purchase_price": 500000.0,
            "downpayment_amount": 100000.0
        },
        {
            "interest_rate": {
                "interest_type": "Fixed",
                "apr": 3.0
            },
            "current_balance": -10000.0,
            "final_month": 122,
            "name": "Test LOC",
            "loan_type": "Student Loan",
            "minimum_monthly_payment": 1000.0
        }
    ]
    }

def test_simple_case():

    class Portfolio(BaseModel):
        loans: List[AllLoanTypes]

    p = Portfolio.parse_obj(get_data())

    assert isinstance(p.loans[0], Mortgage)
    assert isinstance(p.loans[1], StudentLoan)
    assert isinstance(p.loans[2], Mortgage)
    assert isinstance(p.loans[3], StudentLoan)

