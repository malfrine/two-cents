from pydantic.main import BaseModel


class Parameters(BaseModel):
    max_months_in_payment_horizon = 12
    optimality_gap = 0.01
    is_log_milp = True
    max_milp_nodes = 500
    max_milp_seconds = 8
    starting_month = 0
