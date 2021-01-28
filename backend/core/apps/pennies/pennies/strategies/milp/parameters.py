from dataclasses import dataclass
from typing import Dict
from uuid import UUID

import pyomo.environ as pe

from pennies.model.instrument import Instrument
from pennies.model.loan import Loan
from pennies.model.user_personal_finances import UserPersonalFinances


@dataclass
class MILPParameters:
    user_finances: UserPersonalFinances
    _instrument_bounds: Dict[str, float] = None

    def __post_init__(self):
        self._instrument_bounds = dict()

    def _get_instrument(self, id_: UUID) -> Instrument:
        return self.user_finances.portfolio.instruments[id_]

    def _get_loan(self, id_: UUID) -> Loan:
        return self.user_finances.portfolio.instruments[id_]

    def get_monthly_interest_rate(self, id_: UUID) -> float:
        return self._get_instrument(id_).monthly_interest_rate

    def get_starting_balance(self, id_: UUID):
        return self._get_instrument(id_).current_balance

    def get_monthly_allowance(self):
        return self.user_finances.financial_profile.monthly_allowance

    def get_minimum_monthly_payment(self, loan_id: UUID):
        return self._get_loan(loan_id).minimum_monthly_payment

    def get_final_month(self, id_) -> int:
        return self._get_instrument(id_).final_month

    def get_loan_upper_bound(self, id_):
        if id_ not in self._instrument_bounds:
            instrument = self._get_loan(id_)
            self._instrument_bounds[id_] = round(
                instrument.current_balance
                * (1 + instrument.monthly_interest_rate) ** instrument.final_month
            )
        return self._instrument_bounds[id_]
