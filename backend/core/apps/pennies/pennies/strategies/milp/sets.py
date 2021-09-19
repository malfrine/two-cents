from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from uuid import UUID

from pennies.model import taxes
from pennies.model.constants import InvestmentAccountType
from pennies.model.decision_periods import (
    DecisionPeriodsManager,
    DecisionPeriodsManagerFactory,
)
from pennies.model.goal import BaseSavingsGoal, BasePurchaseGoal
from pennies.model.instrument import Instrument
from pennies.model.investment import (
    NonGuaranteedInvestment,
    Cash,
    GuaranteedInvestment,
    BaseInvestment,
)
from pennies.model.loan import Loan, Mortgage
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
    def mortgages(self):
        return list(i.id_ for i in self._instruments if isinstance(i, Mortgage))

    @property
    def non_guaranteed_investments(self):
        return list(
            i.id_ for i in self._instruments if isinstance(i, NonGuaranteedInvestment)
        )

    @property
    def taxing_entities_and_brackets(self):
        return (
            (e, b)
            for e in self.taxing_entities
            for b in self.get_tax_brackets_as_set(e)
        )

    @property
    def investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, (NonGuaranteedInvestment, GuaranteedInvestment))
        )

    @property
    def registered_investments(self):
        def is_registered(i):
            return i.account_type != InvestmentAccountType.NON_REGISTERED

        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, BaseInvestment) and is_registered(i)
        )

    @property
    def rrsp_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, BaseInvestment)
            and i.account_type == InvestmentAccountType.RRSP
        )

    @property
    def tfsa_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, BaseInvestment)
            and i.account_type == InvestmentAccountType.TFSA
        )

    @property
    def non_tfsa_investments(self):
        return list(
            i.id_
            for i in self._instruments
            if isinstance(i, BaseInvestment)
            and i.account_type != InvestmentAccountType.TFSA
        )

    @property
    def guaranteed_investments(self):
        return list(
            i.id_ for i in self._instruments if isinstance(i, GuaranteedInvestment)
        )

    @property
    def non_cash_investments(self) -> Set[str]:
        return set(
            i.id_
            for i in self._instruments
            if isinstance(i, BaseInvestment) and not isinstance(i, Cash)
        )

    @property
    def non_cash_non_guaranteed_investments(self) -> Set[UUID]:
        return set(
            i.id_
            for i in self._instruments
            if isinstance(i, NonGuaranteedInvestment) and not isinstance(i, Cash)
        )

    def get_months_in_horizon(self, order: int) -> List[int]:
        return self.decision_periods.data[order].months

    def get_num_months_in_decision_period(self, index: int) -> int:
        return len(self.get_months_in_horizon(index))

    @property
    def years(self):
        return list(sorted(self.decision_periods.grouped_by_years.keys()))

    @property
    def goals(self):
        return list(self._user_finances.goals.keys())

    def get_allowed_investments_for_goal(self, goal_id):
        goal = self._user_finances.goals.get(goal_id)
        if goal is None:
            return list()
        investments = self._user_finances.portfolio.get_investments_of_types(
            goal.get_allowed_accounts()
        )
        return list(i.id_ for i in investments)

    def get_goals_and_decision_periods(self, goals) -> List[Tuple[UUID, int]]:
        return list(
            (
                (g, t)
                for g in goals
                for t in self.decision_periods.get_decision_periods_after_month(
                    self._user_finances.goals[g].due_month
                )
            )
        )

    # @property
    # def goals_and_decision_periods(self) -> List[Tuple[UUID, int]]:
    #     """all goal uids and their correpsonding decision periods that come after their due month"""
    #     return self.get_goals_and_decision_periods(self.goals)

    @property
    def purchase_goals(self):
        def is_purchase_goal(g):
            return isinstance(self._user_finances.goals[g], BasePurchaseGoal)

        return list(g for g in self.goals if is_purchase_goal(g))

    @property
    def savings_goals(self):
        def is_savings_goal(g):
            return isinstance(self._user_finances.goals[g], BaseSavingsGoal)

        return list(g for g in self.goals if is_savings_goal(g))

    @property
    def savings_goals_and_decision_periods(self) -> List[Tuple[UUID, int]]:
        return self.get_goals_and_decision_periods(self.savings_goals)

    # @property
    # def purchase_goals_and_decision_periods(self) -> List[Tuple[UUID, int]]:
    #     return self.get_goals_and_decision_periods(self.purchase_goals)

    @classmethod
    def create(
        cls,
        user_finances: UserPersonalFinances,
        max_working_months: int,
        max_retirement_months: int,
        start_month: int,
    ) -> "MILPSets":
        decision_periods = DecisionPeriodsManagerFactory(
            max_working_months=max_working_months,
            max_retirement_months=max_retirement_months,
        ).from_user_finances(start_month=start_month, user_finances=user_finances)
        province = user_finances.financial_profile.province_of_residence
        income_tax_brackets = {
            "federal": taxes.FEDERAL,
            "provincial": taxes.PROVINCIAL_TAX_MAP[province],
        }

        return MILPSets(
            _instruments=list(user_finances.portfolio.instruments.values()),
            _user_finances=user_finances,
            decision_periods=decision_periods,
            income_tax_brackets=income_tax_brackets,
        )
