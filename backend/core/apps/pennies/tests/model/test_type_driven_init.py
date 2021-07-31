from typing import List

from pydantic import BaseModel

from pennies.model.investment import GIC, AllInvestmentTypes, Portfolio
from pennies.model.loan import AllLoanTypes, StudentLoan, Mortgage


def get_data():
    return {
        "loans": [
            {
                "name": "Mortgage",
                "loan_type": "Mortgage",
                "interest_rate": {
                    "interest_type": "Mortgage Interest Rate",
                    "interest_rate": {"interest_type": "Fixed", "apr": 2.0},
                    "current_term_end_month": 11,
                },
                "final_month": 12,
                "minimum_monthly_payment": 1.0,
                "current_balance": 10.0,
            },
            {
                "interest_rate": {"interest_type": "Fixed", "apr": 4.1},
                "current_balance": -10000.0,
                "final_month": 108,
                "name": "Student Loan",
                "loan_type": "Student Loan",
                "minimum_monthly_payment": 111.0,
            },
            {
                "name": "House",
                "loan_type": "Mortgage",
                "interest_rate": {
                    "interest_type": "Mortgage Interest Rate",
                    "interest_rate": {"interest_type": "Fixed", "apr": 3.0},
                    "current_term_end_month": 119,
                },
                "start_month": -1,
                "final_month": 323,
                "minimum_monthly_payment": 1200.0,
                "current_balance": 400000.0,
            },
            {
                "interest_rate": {"interest_type": "Fixed", "apr": 3.0},
                "current_balance": -10000.0,
                "final_month": 122,
                "name": "Test LOC",
                "loan_type": "Student Loan",
                "minimum_monthly_payment": 1000.0,
            },
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


def test_gic():
    class InvestmentHolder(BaseModel):
        investment: AllInvestmentTypes

    investment_data = {
        "name": "Test GIC",
        "current_balance": 0.0,
        "final_month": 468,
        "investment_type": "GIC",
        "principal_investment_amount": 10000.0,
        "start_month": 132,
        "account_type": "Non-Registered",
        "interest_rate": {
            "interest_type": "Guaranteed Investment Return Rate",
            "interest_rate": {
                "interest_type": "Variable Investment Return Rate",
                "prime_modifier": 4.0,
            },
            "final_month": 468,
        },
    }

    data = {"investment": investment_data}

    holder = InvestmentHolder.parse_obj(data)
    assert isinstance(holder.investment, GIC)


def test_investment_portfolio():
    class InvestmentHolder(BaseModel):
        investment: AllInvestmentTypes

    investment_data = {
        "name": "Test Portfolio",
        "current_balance": 1.0,
        "investment_type": "Portfolio",
        "pre_authorized_monthly_contribution": 1.0,
        "account_type": "Non-Registered",
        "interest_rate": {
            "interest_type": "Investment Return Rate",
            "roi": 3.0,
            "volatility": 1.0,
        },
    }

    data = {"investment": investment_data}

    holder = InvestmentHolder.parse_obj(data)
    assert isinstance(holder.investment, Portfolio)
