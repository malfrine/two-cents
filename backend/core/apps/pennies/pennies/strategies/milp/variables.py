import itertools
from dataclasses import dataclass
from typing import List
from uuid import UUID

import pyomo.environ as pe

from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.sets import MILPSets


@dataclass
class MILPVariables:

    allocations: pe.Var
    goal_allocations: pe.Var
    balances: pe.Var
    not_paid_off_indicators: pe.Var
    investment_risk_violations: pe.Var
    total_risk_violations: pe.Var
    loan_due_date_violations: pe.Var
    taxable_monthly_incomes: pe.Var
    taxes_accrued_in_brackets: pe.Var
    withdrawals: pe.Var
    retirement_spending_violations: pe.Var
    rrsp_deduction_limits: pe.Var
    tfsa_contribution_limits: pe.Var
    savings_goal_violations: pe.Var
    purchase_goal_violations: pe.Var
    min_payment_violations: pe.Var
    taxable_incomes_in_brackets: pe.Var
    taxable_incomes_indicator: pe.Var

    @classmethod
    def create(
        cls, user_finances: UserPersonalFinances, sets: MILPSets
    ) -> "MILPVariables":
        allocations = pe.Var(
            sets.instruments,
            sets.all_decision_periods_as_set,
            domain=pe.NonNegativeReals,
            initialize=0,
        )
        goal_allocations = pe.Var(
            sets.purchase_goals, domain=pe.NonNegativeReals, initialize=0
        )
        balances = pe.Var(
            sets.instruments,
            sets.all_decision_periods_as_set,
            initialize=0,
            domain=pe.Reals,
        )
        not_paid_off_indicators = pe.Var(
            sets.loans, sets.all_decision_periods_as_set, domain=pe.Binary, initialize=1
        )
        investment_risk_violations = pe.Var(
            sets.working_periods_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        total_risk_violations = pe.Var(
            sets.working_periods_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        loan_due_date_violations = pe.Var(
            sets.loans,
            sets.working_periods_as_set,
            domain=pe.NonNegativeReals,
            initialize=0,
        )
        taxable_monthly_incomes = pe.Var(
            sets.all_decision_periods_as_set, domain=pe.Reals, initialize=0
        )
        taxable_incomes_in_brackets = pe.Var(
            sets.all_decision_periods_as_set,
            sets.taxing_entities_and_brackets,
            domain=pe.Reals,
        )
        taxable_incomes_indicator = pe.Var(
            sets.all_decision_periods_as_set,
            sets.taxing_entities_and_brackets,
            domain=pe.Binary,
            initialize=1,
        )
        taxes_accrued_in_brackets = pe.Var(
            sets.all_decision_periods_as_set,
            sets.taxing_entities_and_brackets,
            domain=pe.NonNegativeReals,
            initialize=20,
        )
        withdrawals = pe.Var(
            sets.investments,
            sets.all_decision_periods_as_set,
            domain=pe.NonNegativeReals,
            initialize=0,
        )
        retirement_spending_violations = pe.Var(
            sets.retirement_periods_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        rrsp_deduction_limits = pe.Var(sets.years, domain=pe.NonNegativeReals)
        tfsa_contribution_limits = pe.Var(sets.years, domain=pe.NonNegativeReals)

        savings_goal_violations = pe.Var(
            sets.savings_goals_and_decision_periods,
            domain=pe.NonNegativeReals,
            initialize=0,
        )
        purchase_goal_violations = pe.Var(
            sets.purchase_goals, domain=pe.NonNegativeReals, initialize=0
        )
        min_payment_violations = pe.Var(
            sets.instruments,
            sets.all_decision_periods_as_set,
            domain=pe.NonNegativeReals,
            initialize=0,
        )
        return MILPVariables(
            allocations=allocations,
            goal_allocations=goal_allocations,
            balances=balances,
            not_paid_off_indicators=not_paid_off_indicators,
            investment_risk_violations=investment_risk_violations,
            total_risk_violations=total_risk_violations,
            loan_due_date_violations=loan_due_date_violations,
            taxable_monthly_incomes=taxable_monthly_incomes,
            taxes_accrued_in_brackets=taxes_accrued_in_brackets,
            withdrawals=withdrawals,
            retirement_spending_violations=retirement_spending_violations,
            rrsp_deduction_limits=rrsp_deduction_limits,
            tfsa_contribution_limits=tfsa_contribution_limits,
            savings_goal_violations=savings_goal_violations,
            purchase_goal_violations=purchase_goal_violations,
            min_payment_violations=min_payment_violations,
            taxable_incomes_in_brackets=taxable_incomes_in_brackets,
            taxable_incomes_indicator=taxable_incomes_indicator,
        )

    @property
    def as_list(self) -> List[pe.Var]:
        return [
            self.allocations,
            self.goal_allocations,
            self.balances,
            self.not_paid_off_indicators,
            self.investment_risk_violations,
            self.total_risk_violations,
            self.loan_due_date_violations,
            self.taxable_monthly_incomes,
            self.taxes_accrued_in_brackets,
            self.withdrawals,
            self.retirement_spending_violations,
            self.rrsp_deduction_limits,
            self.tfsa_contribution_limits,
            self.savings_goal_violations,
            self.purchase_goal_violations,
            self.min_payment_violations,
            self.taxable_incomes_in_brackets,
            self.taxable_incomes_indicator,
        ]

    def get_allocation(self, instrument: UUID, decision_period: int):
        return self.allocations[instrument, decision_period]

    def get_balance(self, instrument: UUID, decision_period: int):
        """corresponds to the instrument balance at the end of the period"""
        return self.balances[instrument, decision_period]

    def get_is_unpaid(self, loan: UUID, decision_period: int):
        return self.not_paid_off_indicators[loan, decision_period]

    def get_total_risk_violation(self, decision_period: int):
        return self.total_risk_violations[decision_period]

    def get_investment_risk_violation(self, decision_period: int):
        return self.investment_risk_violations[decision_period]

    def get_loan_due_date_violation(self, loan: UUID, decision_period: int):
        return self.loan_due_date_violations[loan, decision_period]

    def get_taxable_monthly_income(self, decision_period: int):
        return self.taxable_monthly_incomes[decision_period]

    def get_taxes_accrued_in_bracket(
        self, payment_horizon_order: int, entity: str, bracket_index: int
    ):
        return self.taxes_accrued_in_brackets[
            payment_horizon_order, (entity, bracket_index)
        ]

    def get_taxable_income_in_bracket(
        self, decision_period: int, entity: str, bracket_index: int
    ):
        return self.taxable_incomes_in_brackets[
            decision_period, (entity, bracket_index)
        ]

    def get_withdrawal(self, investment: UUID, decision_period_index: int):
        return self.withdrawals[investment, decision_period_index]

    def get_retirement_spending_violation(self, decision_period_index: int):
        return self.retirement_spending_violations[decision_period_index]

    def get_rrsp_deduction_limit(self, year: int):
        return self.rrsp_deduction_limits[year]

    def get_tfsa_contribution_limit(self, year: int):
        return self.tfsa_contribution_limits[year]

    def get_savings_goal_violation(self, goal, decision_period_index):
        return self.savings_goal_violations[goal, decision_period_index]

    def get_purchase_goal_violation(self, goal):
        return self.purchase_goal_violations[goal]

    def get_min_payment_violation(self, instrument: UUID, decision_period_index: int):
        return self.min_payment_violations[instrument, decision_period_index]

    def get_income_surplus_greater_than_bracket_band(self, t, e, b):
        return self.taxable_incomes_indicator[t, (e, b)]

    def get_allocations(self, instrument_set: List[UUID], decision_periods: List[int]):
        return sum(
            self.get_allocation(i, t)
            for i, t in itertools.product(instrument_set, decision_periods)
        )

    def get_withdrawals(self, instrument_set: List[UUID], decision_periods: List[int]):
        return sum(
            self.get_withdrawal(i, t)
            for i, t in itertools.product(instrument_set, decision_periods)
        )

    def get_balances(self, instrument_set: List[UUID], decision_periods: List[int]):
        return sum(
            self.get_balance(i, t)
            for i, t in itertools.product(instrument_set, decision_periods)
        )

    def get_goal_allocation(self, goal_id: UUID):
        return self.goal_allocations[goal_id]
