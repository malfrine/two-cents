import math

from pennies.utilities.finance import calculate_instrument_balance


def test_mortgage_error():
    starting_balance = -469426.66973508877
    starting_month = 51
    growth_rate = 1.6 / 12 / 100
    allocation = 1246.3919
    end_month = 65
    cur_balance = starting_balance
    for cur_month in range(starting_month + 1, end_month + 1):
        cur_balance = calculate_instrument_balance(
            cur_balance, 1, growth_rate, 0, allocation
        )
        print(f"current balance at {cur_month}: {cur_balance}")
    num_months = end_month - starting_month
    final_balance = calculate_instrument_balance(
        starting_balance, num_months, growth_rate, 0, allocation
    )
    assert math.isclose(final_balance, cur_balance)
