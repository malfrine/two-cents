from dataclasses import dataclass
from typing import Dict
from uuid import UUID

import pyomo.environ as pe

from pennies.model.instrument import Instrument
from pennies.model.investment import Investment
from pennies.model.loan import Loan, RevolvingLoan
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.sets import MILPSets


@dataclass
class MILPParameters:
    user_finances: UserPersonalFinances
    sets: MILPSets
    _instrument_bounds: Dict[str, float] = None

    def __post_init__(self):
        self._instrument_bounds = dict()

    def _get_instrument(self, id_: UUID) -> Instrument:
        return self.user_finances.portfolio.instruments[id_]

    def _get_loan(self, id_: UUID) -> Loan:
        return self.user_finances.portfolio.instruments[id_]

    def _get_investment(self, name) -> Investment:
        return self.user_finances.portfolio.investments_by_name[name]

    def get_average_interest_rate(self, id_: UUID, payment_horizon: int) -> float:
        months = self.sets.payment_horizons.data[payment_horizon].months
        return sum(
            self._get_instrument(id_).monthly_interest_rate(month) for month in months
        ) / len(months)

    def get_volatility(self, id) -> float:
        return self._get_investment(id).volatility

    def get_max_volatility(self):
        return max(
            list(i.volatility for i in self.user_finances.portfolio.investments()),
            default=0,
        )

    def get_min_volatility(self):
        return min(
            list(i.volatility for i in self.user_finances.portfolio.investments()),
            default=0,
        )

    def get_starting_balance(self, id_: UUID):
        return self._get_instrument(id_).current_balance

    def get_user_risk_profile_as_fraction(self) -> float:
        return self.user_finances.financial_profile.risk_tolerance / 100

    def get_monthly_allowance(self):
        return self.user_finances.financial_profile.monthly_allowance

    def get_minimum_monthly_payment(self, loan_id: UUID, payment_horizon_order: int):
        loan = self._get_loan(loan_id)
        return max(loan.get_minimum_monthly_payment(m) for m in self.sets.get_months_in_horizon(payment_horizon_order))

    def get_is_revolving_loan(self, id_) -> bool:
        return isinstance(self.user_finances.portfolio.get_instrument(id_), RevolvingLoan)

    def has_loans(self) -> bool:
        return len(self.user_finances.portfolio.loans) > 0

    def has_investments(self) -> bool:
        return len(self.user_finances.portfolio.investments()) > 0

    def get_final_month(self, id_) -> int:
        return self._get_instrument(id_).final_month or self.user_finances.final_month

    def get_instrument_final_payment_horizon(self, id_):
        return self.sets.payment_horizons.corresponding_horizon(
            self.get_final_month(id_) - 1
        )

    def get_last_payment_horizon_order(self):
        return self.sets.payment_horizons.data[-1].order

    def get_loan_upper_bound(self, id_):
        if id_ not in self._instrument_bounds:
            final_month = self.get_final_month(id_)
            loan = self._get_loan(id_)
            max_monthly_interest_rate = max(
                loan.monthly_interest_rate(month) for month in range(final_month)
            )
            self._instrument_bounds[id_] = round(
                loan.current_balance
                * (1 + max_monthly_interest_rate) ** self.get_final_month(id_)
            )
        return self._instrument_bounds[id_]
