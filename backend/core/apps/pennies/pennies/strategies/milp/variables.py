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

    @classmethod
    def create(
        cls, user_finances: UserPersonalFinances, sets: MILPSets
    ) -> "MILPVariables":

        num_instruments = len(user_finances.portfolio.instruments)
        allocations = pe.Var(
            sets.instruments,
            sets.payment_horizons_as_set,
            bounds=(0.0, user_finances.financial_profile.monthly_allowance),
            initialize=user_finances.financial_profile.monthly_allowance
            / num_instruments
            if num_instruments > 0
            else 1,
        )
        balances = pe.Var(sets.instruments, sets.payment_horizons_as_set, initialize=0)
        not_paid_off_indicators = pe.Var(
            sets.loans, sets.payment_horizons_as_set, domain=pe.Binary, initialize=1
        )
        in_debt_indicators = pe.Var(
            sets.payment_horizons_as_set, domain=pe.Binary, initialize=1
        )
        investment_risk_violations = pe.Var(
            sets.payment_horizons_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        total_risk_violations = pe.Var(
            sets.payment_horizons_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        allocation_slacks = pe.Var(
            sets.payment_horizons_as_set, domain=pe.NonNegativeReals, initialize=0
        )
        loan_due_date_violations = pe.Var(
            sets.loans,
            sets.payment_horizons_as_set,
            domain=pe.NonNegativeReals,
            initialize=0,
        )

        return MILPVariables(
            allocations=allocations,
            balances=balances,
            not_paid_off_indicators=not_paid_off_indicators,
            in_debt_indicators=in_debt_indicators,
            investment_risk_violations=investment_risk_violations,
            total_risk_violations=total_risk_violations,
            allocation_slacks=allocation_slacks,
            loan_due_date_violations=loan_due_date_violations,
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
