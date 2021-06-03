from pydantic.main import BaseModel


class Parameters(BaseModel):
    max_months_in_payment_horizon = 3
    starting_month = 0
    discount_factor = 5 / 100 / 12
