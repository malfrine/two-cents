from pydantic.main import BaseModel


class FinancialProfile(BaseModel):
    monthly_allowance: float
    years_to_retirement: int  # TODO: get this as months_to_retirement (assume they retire on their birthday)
