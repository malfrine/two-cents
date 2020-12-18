from pydantic.main import BaseModel


class FinancialProfile(BaseModel):
    monthly_allowance: float
    years_to_retirement: int
