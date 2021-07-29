from pennies.model.loan import Mortgage


def test_init():
    data = {
        "name": "Mortgage",
        "loan_type": "Mortgage",
        "interest_rate": {
            "interest_type": "Mortgage Interest Rate",
            "interest_rate": {"interest_type": "Fixed", "apr": 2.0},
            "current_term_end_month": 11,
        },
        "final_month": 10,
        "minimum_monthly_payment": 1.0,
        "current_balance": 10.0,
    }
    m = Mortgage.parse_obj(data)
    assert isinstance(m, Mortgage)
    assert m.current_balance is not None
