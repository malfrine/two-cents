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

    @classmethod
    def create(
        cls, user_finances: UserPersonalFinances, sets: MILPSets
    ) -> "MILPVariables":

        allocations = pe.Var(
            sets.instruments,
            sets.payment_horizons_as_set,
            bounds=(0.0, user_finances.financial_profile.monthly_allowance),
            initialize=user_finances.financial_profile.monthly_allowance,
        )
        balances = pe.Var(sets.instruments, sets.payment_horizons_as_set, initialize=0)
        not_paid_off_indicators = pe.Var(
            sets.loans, sets.payment_horizons_as_set, domain=pe.Binary, initialize=1
        )
        in_debt_indicators = pe.Var(
            sets.payment_horizons_as_set, domain=pe.Binary, initialize=1
        )

        return MILPVariables(
            allocations=allocations,
            balances=balances,
            not_paid_off_indicators=not_paid_off_indicators,
            in_debt_indicators=in_debt_indicators,
        )

    def get_allocation(self, instrument: UUID, month: int):
        return self.allocations[instrument, month]

    def get_balance(self, instrument: UUID, month: int):
        return self.balances[instrument, month]

    def get_is_unpaid(self, loan: UUID, month: int):
        return self.not_paid_off_indicators[loan, month]

    def get_is_in_debt(self, month: int):
        return self.in_debt_indicators[month]
