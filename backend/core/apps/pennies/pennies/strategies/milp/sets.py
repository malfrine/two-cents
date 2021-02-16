from dataclasses import dataclass
from typing import List, Set

from pennies.model.investment import Investment
from pennies.model.loan import Loan, InstalmentLoan
from pennies.model.payment_horizons import PaymentHorizons, PaymentHorizonsFactory
from pennies.model.user_personal_finances import UserPersonalFinances


@dataclass
class MILPSets:
    instruments: Set
    payment_horizons: PaymentHorizons
    investments: Set
    loans: Set

    @property
    def payment_horizons_as_set(self) -> Set[int]:
        return set(ph.order for ph in self.payment_horizons.data)

    def get_months_in_horizon(self, order: int) -> List[int]:
        return self.payment_horizons.data[order].months

    def get_num_months_in_horizon(self, order: int) -> int:
        return len(self.get_months_in_horizon(order))

    @classmethod
    def create(
        cls,
        user_finances: UserPersonalFinances,
        max_months_in_payment_horizon: int,
        start_month: int,
    ) -> "MILPSets":
        instruments = set(i.name for i in user_finances.portfolio.instruments.values())
        investments = set(
            instrument.name
            for instrument in user_finances.portfolio.instruments.values()
            if isinstance(instrument, Investment)
        )
        loans = set(
            instrument.name
            for instrument in user_finances.portfolio.instruments.values()
            if isinstance(instrument, Loan)
        )
        payment_horizons = PaymentHorizonsFactory(
            max_months=max_months_in_payment_horizon
        ).from_num_months(
            start_month=start_month, final_month=user_finances.final_month
        )
        return MILPSets(
            instruments=instruments,
            investments=investments,
            loans=loans,
            payment_horizons=payment_horizons,
        )
