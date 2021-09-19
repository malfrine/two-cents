from pydantic.main import BaseModel


class Parameters(BaseModel):
    max_months_in_payment_horizon = 60
    max_months_in_retirement_period = 12
    optimality_gap = 0.01
    is_log_milp = True
    max_milp_nodes = 500_000
    max_milp_seconds = 5
    starting_month = 0
