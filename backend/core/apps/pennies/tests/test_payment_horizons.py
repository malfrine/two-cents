from pennies.model.payment_horizons import (
    PaymentHorizon,
    PaymentHorizons,
    PaymentHorizonsFactory,
)


def test_payment_horizons():
    actual_phs = PaymentHorizons(
        data=[
            PaymentHorizon(order=0, months=[3, 4, 5]),
            PaymentHorizon(order=1, months=[6, 7, 8]),
            PaymentHorizon(order=2, months=[9, 10, 11]),
            PaymentHorizon(order=3, months=[12]),
        ]
    )

    test_phs = PaymentHorizonsFactory(max_months=3).from_num_months(
        start_month=3, final_month=13
    )

    for actual, test in zip(actual_phs.data, test_phs.data):
        assert actual.months == test.months
        assert actual.order == test.order
