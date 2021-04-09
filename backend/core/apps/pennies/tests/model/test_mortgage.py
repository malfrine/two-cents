from pennies.model.loan import Mortgage


def test_init():
    data = {
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
        }
    m = Mortgage.parse_obj(data)
    assert isinstance(m, Mortgage)
    assert m.current_balance is not None
