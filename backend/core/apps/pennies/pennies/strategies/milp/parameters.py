from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID

import pyomo.environ as pe

from pennies.model.instrument import Instrument
from pennies.model.investment import Investment, GuaranteedInvestment
from pennies.model.constants import InvestmentAccountType
from pennies.model.loan import Loan, RevolvingLoan
from pennies.model.rrsp import RRSPAnnualLimitGetter
from pennies.model.taxes import IncomeTaxBrackets
from pennies.model.tfsa import TFSALimitGetter
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
        months = self.sets.decision_periods.data[payment_horizon].months
        return sum(
            self._get_instrument(id_).monthly_interest_rate(month) for month in months
        ) / len(months)

    def get_volatility(self, id) -> float:
        return self._get_investment(id).volatility

    def get_max_volatility(self):
        return max(
            list(
                i.volatility for i in self.user_finances.portfolio.non_cash_investments
            ),
            default=0,
        )

    def get_min_investment_volatility(self):
        return min(
            list(
                i.volatility for i in self.user_finances.portfolio.non_cash_investments
            ),
            default=0,
        )

    def get_starting_balance(self, id_: UUID):
        return self._get_instrument(id_).current_balance

    def get_user_risk_profile_as_fraction(self) -> float:
        return self.user_finances.financial_profile.risk_tolerance / 100

    def get_monthly_allowance(self, decision_period_index: int):
        decision_period = self.sets.decision_periods.data[decision_period_index]
        total_allowance_in_decision_period = sum(
            self.user_finances.financial_profile.get_monthly_allowance(month)
            for month in decision_period.months
        )
        return total_allowance_in_decision_period / len(decision_period.months)

    def get_minimum_monthly_payment(
        self, instrument_id: UUID, payment_horizon_order: int
    ):
        instrument = self._get_instrument(instrument_id)
        return max(
            instrument.get_minimum_monthly_payment(m)
            for m in self.sets.get_months_in_horizon(payment_horizon_order)
        )

    def get_before_tax_monthly_income(self, decision_period_index: int):
        decision_period = self.sets.decision_periods.data[decision_period_index]
        total_salary_in_decision_period = sum(
            self.user_finances.financial_profile.get_monthly_income(month)
            for month in decision_period.months
        )
        return total_salary_in_decision_period / len(decision_period.months)

    def get_is_revolving_loan(self, id_) -> bool:
        return isinstance(
            self.user_finances.portfolio.get_instrument(id_), RevolvingLoan
        )

    def get_is_investment(self, id_):
        return (
            self.user_finances.portfolio.investments_by_name.get(id_, None) is not None
        )

    def get_is_guaranteed_investment(self, id_):
        return isinstance(
            self.user_finances.portfolio.get_instrument(id_), GuaranteedInvestment
        )

    def has_loans(self) -> bool:
        return len(self.user_finances.portfolio.loans) > 0

    def has_investments(self) -> bool:
        return len(self.user_finances.portfolio.investments()) > 0

    def get_final_month(self, id_) -> int:
        return (
            self._get_instrument(id_).final_month
            or self.user_finances.financial_profile.retirement_month
        )

    def get_instrument_final_payment_horizon(self, id_):
        return self.sets.decision_periods.get_corresponding_period(
            self.get_final_month(id_) - 1
        )

    def get_final_decision_period_index(self):
        return self.sets.decision_periods.data[-1].index

    def get_final_work_period_index(self) -> Optional[int]:
        return max(self.sets.working_periods_as_set, default=None)

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

    def get_constraint_violation_penalty(self):
        final_month = self.user_finances.financial_profile.retirement_month
        monthly_allowance = (
            self.user_finances.financial_profile.monthly_allowance_before_retirement
        )
        starting_investment_worth = sum(
            self.get_starting_balance(i) for i in self.sets.investments
        )
        return starting_investment_worth + monthly_allowance * final_month

    def get_bracket_marginal_tax_rate(self, e: str, b: int):
        return self.sets.income_tax_brackets[e].data[b].marginal_tax_rate_as_fraction

    def get_bracket_marginal_income(self, e: str, b: int):
        return self.sets.income_tax_brackets[e].data[b].monthly_marginal_upper_bound

    def get_bracket_cumulative_income(self, e: str, b: int):
        return self.sets.income_tax_brackets[e].get_bracket_cumulative_income(b) / 12

    def get_minimum_monthly_withdrawals(self, t):
        if t > self.get_retirement_decision_period_index():
            return self.user_finances.financial_profile.monthly_retirement_spending
        else:
            return 0

    def get_rrsp_limit(self, year: int):
        return RRSPAnnualLimitGetter.get_limit(year)

    def get_starting_rrsp_deduction_limit(self) -> float:
        return self.user_finances.financial_profile.starting_rrsp_contribution_limit

    def get_age(self, year: int) -> float:
        start_year = min(self.sets.years)
        return self.user_finances.financial_profile.current_age + (year - start_year)

    def get_retirement_age(self) -> float:
        return self.user_finances.financial_profile.retirement_age

    def get_additional_tfsa_limit(self, year: int):
        return TFSALimitGetter.get_limit(year)

    def get_starting_tfsa_contribution_limit(self):
        return self.user_finances.financial_profile.starting_tfsa_contribution_limit

    def get_has_guaranteed_investment_matured(self, instrument_id: UUID, decision_period_index: int):
        instrument = self._get_instrument(instrument_id)
        if isinstance(instrument, GuaranteedInvestment):
            return self.get_decision_period_index_of_maturation(instrument_id) < decision_period_index
        else:
            raise ValueError(f"Investment {instrument_id} is not a Guaranteed Investment")

    def get_decision_period_index_of_maturation(self, instrument_id):
        instrument = self._get_instrument(instrument_id)
        if isinstance(instrument, GuaranteedInvestment):
            maturation_month = instrument.final_month
            min_planing_horizon_month = min(self.sets.decision_periods.month_to_period_dict.keys())
            if maturation_month <= min_planing_horizon_month:
                # already matured before planning started
                return min(self.sets.all_decision_periods_as_set)
            else:
                return self.sets.decision_periods.month_to_period_dict[maturation_month].index
        else:
            raise ValueError(f"Investment {instrument_id} is not a Guaranteed Investment")

    def get_is_rrsp_investment(self, instrument_id):
        instrument = self._get_instrument(instrument_id)
        return isinstance(instrument, Investment) and instrument.account_type == InvestmentAccountType.RRSP

    def get_is_retired(self, decision_period_index: int):
        return decision_period_index >= self.get_retirement_decision_period_index()

    def get_retirement_decision_period_index(self):
        return min(self.sets.retirement_periods_as_set)

    def get_num_months_between_decision_periods(self, start_dp_index: int, end_dp_index: int):
        return sum(
            self.sets.get_num_months_in_decision_period(dp_index)
            for dp_index in range(start_dp_index, end_dp_index)
        )



