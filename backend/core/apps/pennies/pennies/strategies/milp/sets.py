from dataclasses import dataclass
from typing import List, Set, Dict

from pennies.model import taxes
from pennies.model.investment import Investment, Cash, GuaranteedInvestment
from pennies.model.loan import Loan, InstalmentLoan
from pennies.model.payment_horizons import PaymentHorizons, PaymentHorizonsFactory
from pennies.model.taxes import IncomeTaxBrackets
from pennies.model.user_personal_finances import UserPersonalFinances


@dataclass
class MILPSets:
    instruments: Set
    payment_horizons: PaymentHorizons
    investments: Set
    loans: Set
    income_tax_brackets: Dict[str, IncomeTaxBrackets]
    _user_finances: UserPersonalFinances

    @property
    def payment_horizons_as_set(self) -> Set[int]:
        return set(ph.order for ph in self.payment_horizons.data)

    @property
    def taxing_entities(self):
        return set(self.income_tax_brackets.keys())

    def get_tax_brackets_as_set(self, taxing_entity: str) -> Set[int]:
        return set(range(self.income_tax_brackets[taxing_entity].num_brackets))

    @property
    def taxing_entities_and_brackets(self):
        return (

            (e, b) for e in self.taxing_entities for b in self.get_tax_brackets_as_set(e)
        )

    @property
    def non_cash_investments(self) -> Set[str]:
        return set(
            i
            for i in self.investments
            if not isinstance(self._user_finances.portfolio.get_investment(i), Cash)
        )

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
        instruments = set(
            i.name
            for i in user_finances.portfolio.instruments.values()
            if not isinstance(i, GuaranteedInvestment)
        )
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
        province = user_finances.financial_profile.province_of_residence
        income_tax_brackets = {
            "federal": taxes.FEDERAL,
            "provincial": taxes.PROVINCIAL_TAX_MAP[province]
        }

        return MILPSets(
            _user_finances=user_finances,
            instruments=instruments,
            investments=investments,
            loans=loans,
            payment_horizons=payment_horizons,
            income_tax_brackets=income_tax_brackets
        )
