from pydantic.main import BaseModel


class Parameters(BaseModel):
    max_months_in_payment_horizon = 6
    starting_month = 0
