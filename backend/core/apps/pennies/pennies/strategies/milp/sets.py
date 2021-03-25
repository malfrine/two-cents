from dataclasses import dataclass
from typing import List, Set, Dict

from pennies.model import taxes
from pennies.model.instrument import Instrument
from pennies.model.investment import (
    Investment,
    Cash,
    GuaranteedInvestment,
)
from pennies.model.constants import InvestmentAccountType
from pennies.model.loan import Loan, InstalmentLoan
from pennies.model.decision_periods import (
    DecisionPeriodsManager,
    DecisionPeriodsManagerFactory,
)
from pennies.model.taxes import IncomeTaxBrackets
from pennies.model.user_personal_finances import UserPersonalFinances


@dataclass
class MILPSets:
    _instruments: List[Instrument]
    decision_periods: DecisionPeriodsManager
    income_tax_brackets: Dict[str, IncomeTaxBrackets]
    _user_finances: UserPersonalFinances

    @property
    def working_periods_as_set(self) -> Set[int]:
        return set(wp.index for wp in self.decision_periods.working_periods)

    @property
    def retirement_periods_as_set(self) -> Set[int]:
        return set(rp.index for rp in self.decision_periods.retirement_periods)

    @property
    def all_decision_periods_as_set(self) -> Set[int]:
        return set(dp.index for dp in self.decision_periods.all_periods)

    @property
    def taxing_entities(self):
        return set(self.income_tax_brackets.keys())

    def get_tax_brackets_as_set(self, taxing_entity: str) -> Set[int]:
        return set(range(self.income_tax_brackets[taxing_entity].num_brackets))

    @property
    def instruments(self):
        return list(i.id_ for i in self._instruments)

    @property
    def loans(self):
        return list(i.id_ for i in self._instruments if isinstance(i, Loan))

    @property
    def investments(self):
        return list(i.id_ for i in self._instruments if isinstance(i, Investment))

    @property
    def taxing_entities_and_brackets(self):
        return (
            (e, b)
            for e in self.taxing_entities
            for b in self.get_tax_brackets_as_set(e)
        )

    @property
    def investments_and_guaranteed_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, (Investment, GuaranteedInvestment))
        )

    @property
    def rrsp_investments_and_guaranteed_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, (Investment, GuaranteedInvestment))
            and i.account_type == InvestmentAccountType.RRSP
        )

    @property
    def tfsa_investments_and_guaranteed_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, (Investment, GuaranteedInvestment))
            and i.account_type == InvestmentAccountType.TFSA
        )

    @property
    def non_tfsa_investments_and_guaranteed_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, (Investment, GuaranteedInvestment))
            and i.account_type != InvestmentAccountType.TFSA
        )

    @property
    def guaranteed_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, GuaranteedInvestment)
        )

    @property
    def non_cash_investments(self) -> Set[str]:
        return set(
            i
            for i in self.investments
            if not isinstance(self._user_finances.portfolio.get_investment(i), Cash)
        )

    def get_months_in_horizon(self, order: int) -> List[int]:
        return self.decision_periods.data[order].months

    def get_num_months_in_decision_period(self, index: int) -> int:
        return len(self.get_months_in_horizon(index))

    @property
    def years(self):
        return list(sorted(self.decision_periods.grouped_by_years.keys()))


    @classmethod
    def create(
        cls,
        user_finances: UserPersonalFinances,
        max_months_in_payment_horizon: int,
        start_month: int,
    ) -> "MILPSets":
        # instruments = set(
        #     i.name
        #     for i in user_finances.portfolio.instruments.values()
        #     # if not isinstance(i, GuaranteedInvestment)
        # )
        # investments = set(
        #     instrument.name
        #     for instrument in user_finances.portfolio.instruments.values()
        #     if isinstance(instrument, Investment)
        # )
        # loans = set(
        #     instrument.name
        #     for instrument in user_finances.portfolio.instruments.values()
        #     if isinstance(instrument, Loan)
        # )
        decision_periods = DecisionPeriodsManagerFactory(
            max_months=max_months_in_payment_horizon
        ).from_num_months(
            start_month=start_month,
            retirement_month=user_finances.financial_profile.retirement_month,
            final_month=user_finances.financial_profile.death_month,
        )
        province = user_finances.financial_profile.province_of_residence
        income_tax_brackets = {
            "federal": taxes.FEDERAL,
            "provincial": taxes.PROVINCIAL_TAX_MAP[province],
        }

        return MILPSets(
            _instruments=list(user_finances.portfolio.instruments.values()),
            _user_finances=user_finances,
            # instruments=instruments,
            # investments=investments,
            # loans=loans,
            decision_periods=decision_periods,
            income_tax_brackets=income_tax_brackets,
        )
