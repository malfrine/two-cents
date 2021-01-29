from typing import List

from pydantic import root_validator
from pydantic.main import BaseModel
from pennies.model.financial_profile import FinancialProfile

from pennies.model.investment import Investment
from pennies.model.loan import Loan


class PenniesRequest(BaseModel):
    financial_profile: FinancialProfile
    loans: List[Loan]
    investments: List[Investment]
    strategies: List[str]

    @root_validator
    def validate_instruments_exist(cls, values):
        if not (values["loans"] or values["investments"]):
            raise ValueError("No loans or investments exist")
        return values

    @root_validator
    def validate_enough_monthly_allowance(cls, values):
        loans: List[Loan] = values["loans"]
        total_min_payments = sum(l.minimum_monthly_payment for l in loans)
        financial_profile: FinancialProfile = values["financial_profile"]
        if total_min_payments >= financial_profile.monthly_allowance:
            raise ValueError(
                f"Total minimum loan payments ({total_min_payments} "
                f"is greater than or equal to monthly allowance {financial_profile.monthly_allowance}"
            )
        return values

