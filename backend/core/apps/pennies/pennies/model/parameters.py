from pydantic.main import BaseModel


class Parameters(BaseModel):
    max_months_in_payment_horizon = 60
    max_months_in_retirement_period = 60
    optimality_gap = 0.01
    is_log_milp = False
    max_milp_nodes = 500_000
    max_milp_seconds = 3
    starting_month = 0
    instrument_upper_bound_factor = 1.4
    # multiplying the max possible value of an instrument upper bound just to be safe
    additional_allocation_factor = 1.5
    # multiplying the max possible value of an instrument allocation just to be safe
    registered_account_benefit = 0.025
    # the utility in dollars that a user gets from using a registered account (TFSA, RRSP, etc)
    preference_violation_cost = 0.5
    # the utility in dollars that a user loses from not adhering to their preference
    mandatory_requirement_violation_cost = 25
    # the utility in dollars that a user loses from not adhering to a mandatory requirement
    max_volatility = 10  # the maximum possible volatility of an instrument
    debt_utility_cost = 0  # the utility cost of having a loan in a given month
    goal_violation_cost = 0.2
    risk_violation_cost = 0.5
