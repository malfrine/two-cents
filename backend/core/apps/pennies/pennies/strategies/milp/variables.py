from dataclasses import dataclass
from uuid import UUID

import pyomo.environ as pe

from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.sets import MILPSets


@dataclass
class MILPVariables:

    allocations: pe.Var
    balances: pe.Var
    not_paid_off_indicators: pe.Var
    in_debt_indicators: pe.Var
    investment_risk_violations: pe.Var
    total_risk_violations: pe.Var
    allocation_slacks: pe.Var
    loan_due_date_violations: pe.Var
    taxable_monthly_incomes: pe.Var
    pos_overflow_in_brackets: pe.Var
    remaining_marginal_income_in_brackets: pe.Var
    taxes_accrued_in_brackets: pe.Var
    withdrawals: pe.Var
    retirement_spending_violations: pe.Var
    rrsp_deduction_limits: pe.Var
    tfsa_contribution_limits: pe.Var
    pos_withdrawal_differences: pe.Var
    neg_withdrawal_differences: pe.Var
    withdrawal_fluctuation_violation: pe.Var
    max_monthly_payment_violations: pe.Var
    savings_goal_violations: pe.Var
    purchase_goal_violations: pe.Var

    @classmethod
    def create(
        cls, user_finances: UserPersonalFinances, sets: MILPSets
    ) -> "MILPVariables":

        num_instruments = len(user_finances.portfolio.instruments)
        allocations = pe.Var(
            sets.instruments,
            sets.all_decision_periods_as_set,
            bounds=(
                0.0,
                user_finances.financial_profile.monthly_allowance_before_retirement,
            ),
            initialize=user_finances.financial_profile.monthly_allowance_before_retirement
            / num_instruments
            if num_instruments > 0
            else 1,
        )
        balances = pe.Var(
            sets.instruments, sets.all_decision_periods_as_set, initialize=0
        )
        not_paid_off_indicators = pe.Var(
            sets.loans, sets.working_periods_as_set, domain=pe.Binary, initialize=1
        )
        in_debt_indicators = pe.Var(
            sets.working_periods_as_set, domain=pe.Binary, initialize=1
        )
        investment_risk_violations = pe.Var(
            sets.working_periods_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        total_risk_violations = pe.Var(
            sets.working_periods_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        allocation_slacks = pe.Var(
            sets.all_decision_periods_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        loan_due_date_violations = pe.Var(
            sets.loans,
            sets.working_periods_as_set,
            domain=pe.NonNegativeReals,
            initialize=0,
        )
        taxable_monthly_incomes = pe.Var(sets.all_decision_periods_as_set)
        pos_overflow_in_brackets = pe.Var(
            sets.all_decision_periods_as_set,
            sets.taxing_entities_and_brackets,
            domain=pe.NonNegativeReals,
        )
        remaining_marginal_income_in_brackets = pe.Var(
            sets.all_decision_periods_as_set,
            sets.taxing_entities_and_brackets,
            domain=pe.NonNegativeReals,
        )
        taxes_accrued_in_brackets = pe.Var(
            sets.all_decision_periods_as_set,
            sets.taxing_entities_and_brackets,
            domain=pe.NonNegativeReals,
        )
        withdrawals = pe.Var(
            sets.investments_and_guaranteed_investments,
            sets.all_decision_periods_as_set,
            domain=pe.NonNegativeReals,
        )
        retirement_spending_violations = pe.Var(
            sets.retirement_periods_as_set, domain=pe.NonNegativeReals
        )
        rrsp_deduction_limits = pe.Var(sets.years, domain=pe.NonNegativeReals)
        tfsa_contribution_limits = pe.Var(sets.years, domain=pe.NonNegativeReals)
        pos_withdrawal_differences = pe.Var(sets.all_decision_periods_as_set, domain=pe.NonNegativeReals)
        neg_withdrawal_differences = pe.Var(sets.all_decision_periods_as_set, domain=pe.NonNegativeReals)
        withdrawal_fluctuation_violation = pe.Var(domain=pe.NonNegativeReals)
        max_monthly_payment_violations = pe.Var(sets.instruments, sets.all_decision_periods_as_set, domain=pe.NonNegativeReals, initialize=0)
        savings_goal_violations = pe.Var(sets.savings_goals_and_decision_periods, domain=pe.NonNegativeReals)
        purchase_goal_violations = pe.Var(sets.purchase_goals, domain=pe.NonNegativeReals)
        return MILPVariables(
            allocations=allocations,
            balances=balances,
            not_paid_off_indicators=not_paid_off_indicators,
            in_debt_indicators=in_debt_indicators,
            investment_risk_violations=investment_risk_violations,
            total_risk_violations=total_risk_violations,
            allocation_slacks=allocation_slacks,
            loan_due_date_violations=loan_due_date_violations,
            taxable_monthly_incomes=taxable_monthly_incomes,
            pos_overflow_in_brackets=pos_overflow_in_brackets,
            remaining_marginal_income_in_brackets=remaining_marginal_income_in_brackets,
            taxes_accrued_in_brackets=taxes_accrued_in_brackets,
            withdrawals=withdrawals,
            retirement_spending_violations=retirement_spending_violations,
            rrsp_deduction_limits=rrsp_deduction_limits,
            tfsa_contribution_limits=tfsa_contribution_limits,
            neg_withdrawal_differences=neg_withdrawal_differences,
            pos_withdrawal_differences=pos_withdrawal_differences,
            withdrawal_fluctuation_violation=withdrawal_fluctuation_violation,
            max_monthly_payment_violations=max_monthly_payment_violations,
            savings_goal_violations=savings_goal_violations,
            purchase_goal_violations=purchase_goal_violations
        )

    def get_allocation(self, instrument: UUID, month: int):
        return self.allocations[instrument, month]

    def get_balance(self, instrument: UUID, month: int):
        return self.balances[instrument, month]

    def get_is_unpaid(self, loan: UUID, month: int):
        return self.not_paid_off_indicators[loan, month]

    def get_is_in_debt(self, month: int):
        return self.in_debt_indicators[month]

    def get_total_risk_violation(self, payment_horizon_order: int):
        return self.total_risk_violations[payment_horizon_order]

    def get_investment_risk_violation(self, payment_horizon_order: int):
        return self.investment_risk_violations[payment_horizon_order]

    def get_allocation_slack(self, payment_horizon_order: int):
        return self.allocation_slacks[payment_horizon_order]

    def get_loan_due_date_violation(self, loan: str, payment_horizon_order: int):
        return self.loan_due_date_violations[loan, payment_horizon_order]

    def get_taxable_monthly_income(self, payment_horizon_order: int):
        return self.taxable_monthly_incomes[payment_horizon_order]

    def get_pos_overflow_in_bracket(
        self, payment_horizon_order: int, entity: str, bracket_index: int
    ):
        return self.pos_overflow_in_brackets[
            payment_horizon_order, (entity, bracket_index)
        ]

    def get_remaining_marginal_income_in_bracket(
        self, payment_horizon_order: int, entity: str, bracket_index: int
    ):
        return self.remaining_marginal_income_in_brackets[
            payment_horizon_order, (entity, bracket_index)
        ]

    def get_taxes_accrued_in_bracket(
        self, payment_horizon_order: int, entity: str, bracket_index: int
    ):
        return self.taxes_accrued_in_brackets[
            payment_horizon_order, (entity, bracket_index)
        ]

    def get_withdrawal(self, investment: str, decision_period_index: int):
        return self.withdrawals[investment, decision_period_index]

    def get_retirement_spending_violation(self, decision_period_index: int):
        return self.retirement_spending_violations[decision_period_index]

    def get_rrsp_deduction_limit(self, year: int):
        return self.rrsp_deduction_limits[year]

    def get_tfsa_contribution_limit(self, year: int):
        return self.tfsa_contribution_limits[year]

    def get_neg_withdrawal_difference(self, decision_period_index: int):
        return self.neg_withdrawal_differences[decision_period_index]

    def get_pos_withdrawal_difference(self, decision_period_index: int):
        return self.pos_withdrawal_differences[decision_period_index]

    def get_withdrawal_fluctuation_violation(self):
        return self.withdrawal_fluctuation_violation

    def get_max_monthly_payment_violation(self, instrument, decision_period_index):
        return self.max_monthly_payment_violations[instrument, decision_period_index]

    def get_savings_goal_violation(self, goal, decision_period_index):
        return self.savings_goal_violations[goal, decision_period_index]

    def get_purchase_goal_violation(self, goal):
        return self.purchase_goal_violations[goal]
