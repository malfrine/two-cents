from dataclasses import dataclass
from math import ceil
from typing import Dict
from uuid import UUID

from pennies.model.constants import InvestmentAccountType
from pennies.model.instrument import Instrument
from pennies.model.investment import (
    NonGuaranteedInvestment,
    GuaranteedInvestment,
    BaseInvestment,
)
from pennies.model.loan import RevolvingLoan
from pennies.model.parameters import Parameters as ModelParameters
from pennies.model.rrsp import RRSPAnnualLimitGetter, RRSP_LIMIT_INCOME_FACTOR
from pennies.model.taxes import (
    CAPITAL_GAINS_TAX_PERCENTAGE,
    MAX_MARGINAL_MONTHLY_INCOME,
)
from pennies.model.tfsa import TFSALimitGetter
from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.sets import MILPSets
from pennies.utilities.datetime import MONTHS_IN_YEAR


@dataclass
class MILPParameters:
    user_finances: UserPersonalFinances
    sets: MILPSets
    model_parameters: ModelParameters
    loan_bounds: Dict[str, float] = None

    def __post_init__(self):
        self.loan_bounds = dict()
        final_month = self.user_finances.financial_profile.death_month
        for loan_id in self.sets.loans:
            loan = self._get_instrument(loan_id)
            max_monthly_interest_rate = max(
                loan.monthly_interest_rate(month) for month in range(final_month)
            )
            upper_bound = (
                loan.current_balance * (1 + max_monthly_interest_rate) ** final_month
            )
            self.loan_bounds[loan_id] = (
                ceil(upper_bound) * self.get_instrument_upper_bound_factor()
            )

    def _get_instrument(self, id_: UUID) -> Instrument:
        return self.user_finances.portfolio.instruments[id_]

    def get_average_interest_rate(self, id_: UUID, payment_horizon: int) -> float:
        months = self.sets.decision_periods.data[payment_horizon].months
        total_interest_rate = sum(
            self._get_instrument(id_).monthly_interest_rate(month) for month in months
        )
        return total_interest_rate / len(months)

    def get_instrument_volatility(self, id) -> float:
        return self._get_instrument(id).volatility

    def get_max_investment_volatility(self):
        return self.model_parameters.max_volatility

    def get_starting_balance(self, id_: UUID):
        return self._get_instrument(id_).current_balance

    def get_user_risk_profile_as_fraction(self) -> float:
        return self.user_finances.financial_profile.risk_tolerance / 100

    def get_minimum_monthly_payment(
        self, instrument_id: UUID, payment_horizon_order: int
    ):
        instrument = self._get_instrument(instrument_id)
        return max(
            instrument.get_minimum_monthly_payment(m)
            for m in self.sets.get_months_in_decision_period(payment_horizon_order)
        )

    def get_before_tax_monthly_income(self, decision_period_index: int):
        decision_period = self.sets.decision_periods.data[decision_period_index]
        total_salary_in_decision_period = sum(
            self.user_finances.financial_profile.get_pre_tax_monthly_income(month)
            for month in decision_period.months
        )
        return total_salary_in_decision_period / len(decision_period.months)

    def get_is_revolving_loan(self, id_) -> bool:
        return isinstance(
            self.user_finances.portfolio.get_instrument(id_), RevolvingLoan
        )

    def get_is_non_guaranteed_investment(self, id_):
        return isinstance(self._get_instrument(id_), NonGuaranteedInvestment)

    def get_is_guaranteed_investment(self, id_):
        return isinstance(self._get_instrument(id_), GuaranteedInvestment)

    def get_is_investment(self, id_):
        return isinstance(self._get_instrument(id_), BaseInvestment)

    def has_loans(self) -> bool:
        return len(self.sets.loans) > 0

    def has_investments(self) -> bool:
        return len(self.sets.investments) > 0

    def get_final_month(self, id_) -> int:
        """Must pay off every loan by retirement month"""
        final_month = self._get_instrument(id_).final_month
        retirement_month = self.get_retirement_month()
        return final_month or retirement_month

    def get_instrument_due_decision_period(self, id_):
        return self.sets.decision_periods.get_corresponding_period(
            self.get_final_month(id_)
        )

    def get_final_decision_period_index(self):
        return self.sets.decision_periods.max_period_index

    def get_loan_upper_bound(self, id_):
        return self.loan_bounds[id_]

    def get_bracket_marginal_tax_rate(self, e: str, b: int):
        return self.sets.income_tax_brackets[e].data[b].marginal_tax_rate_as_fraction

    def get_bracket_marginal_income(self, e: str, b: int):
        return self.sets.income_tax_brackets[e].data[b].monthly_marginal_upper_bound

    def get_bracket_cumulative_income(self, e: str, b: int):
        return (
            self.sets.income_tax_brackets[e].get_bracket_cumulative_income(b)
            / MONTHS_IN_YEAR
        )

    def get_previous_bracket_cumulative_income(self, e: str, b: int):
        if b == 0:
            return 0
        else:
            return self.get_bracket_cumulative_income(e, b - 1)

    def get_minimum_monthly_withdrawals(self, t):
        if self.get_is_retired(t):
            return self.user_finances.financial_profile.monthly_retirement_spending
        else:
            return 0

    def get_annual_income(self, year: int):
        decision_periods = self.sets.decision_periods.get_decision_period_instances_in_year(
            year
        )
        return sum(
            self.get_before_tax_monthly_income(dp.index) for dp in decision_periods
        )

    def get_additional_rrsp_limit(self, year: int):
        annual_income = self.get_annual_income(year)
        return min(
            RRSPAnnualLimitGetter.get_limit(year),
            annual_income * RRSP_LIMIT_INCOME_FACTOR,
        )

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

    def get_has_guaranteed_investment_matured(
        self, instrument_id: UUID, decision_period_index: int
    ):
        instrument = self._get_instrument(instrument_id)
        if isinstance(instrument, GuaranteedInvestment):
            return (
                self.get_decision_period_index_of_maturation(instrument_id)
                < decision_period_index
            )
        else:
            raise ValueError(
                f"Investment {instrument_id} is not a Guaranteed Investment"
            )

    def get_decision_period_index_of_maturation(self, instrument_id):
        instrument = self._get_instrument(instrument_id)
        if isinstance(instrument, GuaranteedInvestment):
            maturation_month = instrument.final_month
            min_planing_horizon_month = min(
                self.sets.decision_periods.month_to_period_dict.keys()
            )
            if maturation_month <= min_planing_horizon_month:
                # already matured before planning started
                return min(self.sets.all_decision_periods_as_set)
            else:
                return self.sets.decision_periods.month_to_period_dict[
                    maturation_month
                ].index
        else:
            raise ValueError(
                f"Investment {instrument_id} is not a Guaranteed Investment"
            )

    def get_is_rrsp_investment(self, instrument_id):
        instrument = self._get_instrument(instrument_id)
        return (
            isinstance(instrument, NonGuaranteedInvestment)
            and instrument.account_type == InvestmentAccountType.RRSP
        )

    def get_is_retired(self, decision_period_index: int):
        return decision_period_index >= self.get_retirement_decision_period_index()

    def get_retirement_decision_period_index(self):
        return min(self.sets.retirement_periods_as_set)

    def get_max_monthly_payment(self, instrument_id, decision_period_index):
        months = self.sets.get_months_in_decision_period(decision_period_index)
        instrument = self.user_finances.portfolio.instruments[instrument_id]
        return min(
            (
                instrument.get_maximum_monthly_payment(month)
                for month in months
                if instrument.get_maximum_monthly_payment(month) is not None
            ),
            default=None,
        )

    def get_goal_amount(self, g, t):
        return self.user_finances.goals[g].amount

    def get_goal_due_month(self, g):
        return self.user_finances.goals[g].due_month

    def get_savings_fraction(self, t: int):
        if self.get_is_retired(t):
            return 0
        else:
            return (
                self.user_finances.financial_profile.percent_salary_for_spending / 100
            )

    def get_capital_gains_tax_fraction(self):
        return CAPITAL_GAINS_TAX_PERCENTAGE / 100

    def get_allocation_upper_bound(self, decision_period: int):
        savings_fraction = self.get_savings_fraction(decision_period)
        pre_tax_income = self.get_before_tax_monthly_income(decision_period)
        return (
            savings_fraction * pre_tax_income * self.get_additional_allocation_factor()
        )

    def get_starting_debt(self):
        return sum(self.get_starting_balance(l) for l in self.sets.loans)

    def get_is_tfsa_investment(self, investment_id: UUID):
        instrument = self._get_instrument(investment_id)
        return (
            isinstance(instrument, NonGuaranteedInvestment)
            and instrument.account_type == InvestmentAccountType.TFSA
        )

    def get_annual_pre_tax_income(self, year: int):
        decision_periods = self.sets.decision_periods.grouped_by_years[year]
        return sum(
            self.get_before_tax_monthly_income(dp.index) for dp in decision_periods
        )

    def get_is_guaranteed_and_matured_investment(self, i, t):
        if not self.get_is_guaranteed_investment(i):
            return False
        else:
            return self.get_has_guaranteed_investment_matured(i, t)

    def get_is_before_loan_due_date(self, loan_id: UUID, decision_period: int):
        return (
            decision_period < self.get_instrument_due_decision_period(loan_id).index - 1
        )

    def get_is_after_loan_due_date(self, loan_id: UUID, decision_period: int):
        return (
            decision_period > self.get_instrument_due_decision_period(loan_id).index - 1
        )

    def get_goal_decision_period(self, goal_id: UUID):
        month = self.get_goal_due_month(goal_id)
        decision_period = self.sets.decision_periods.get_corresponding_period_or_closest(
            month
        ).index
        return decision_period

    def has_rrsp_investments(self):
        return len(self.sets.rrsp_investments) > 0

    def get_volatility_limit(self):
        risk_tolerance = self.get_user_risk_profile_as_fraction()
        max_volatility = self.get_max_investment_volatility()
        return risk_tolerance * max_volatility

    def get_retirement_month(self) -> int:
        return self.user_finances.financial_profile.retirement_month

    def get_taxable_income_upper_bound(self, e, b):
        bracket_marginal_income = self.get_bracket_marginal_income(e, b)
        max_income = MAX_MARGINAL_MONTHLY_INCOME
        return bracket_marginal_income + max_income

    def has_tfsa_investments(self):
        return len(self.sets.tfsa_investments) > 0

    def get_investment(self, investment_id):
        return self.user_finances.portfolio.get_investment(investment_id)

    def get_is_purchase_goal_due(self, decision_period: int):
        for g in self.sets.purchase_goals:
            goal_decision_period = self.get_goal_decision_period(g)
            if goal_decision_period == decision_period:
                return True
        return False

    def get_instrument_upper_bound_factor(self):
        return self.model_parameters.instrument_upper_bound_factor

    def get_additional_allocation_factor(self):
        return self.model_parameters.additional_allocation_factor

    def get_starting_before_tax_monthly_income(self):
        """User's monthly tax at the start of the planning - not accounting for any growth in income over the years"""
        return self.user_finances.financial_profile.monthly_salary_before_tax

    def get_mandatory_requirement_violation_cost(self):
        return (
            self.model_parameters.mandatory_requirement_violation_cost
            * self.get_starting_before_tax_monthly_income()
        )

    def get_preference_violation_cost(self):
        return (
            self.model_parameters.preference_violation_cost
            * self.get_starting_before_tax_monthly_income()
        )

    def get_registered_account_benefit(self):
        return (
            self.model_parameters.registered_account_benefit
            * self.get_starting_before_tax_monthly_income()
        )

    def get_debt_utility_cost(self):
        return (
            self.model_parameters.debt_utility_cost
            * self.get_starting_before_tax_monthly_income()
        )

    def get_goal_violation_cost(self):
        return (
            self.model_parameters.goal_violation_cost
            * self.get_starting_before_tax_monthly_income()
        )

    def get_risk_violation_cost(self):
        return (
            self.model_parameters.risk_violation_cost
            * self.get_starting_before_tax_monthly_income()
        )
