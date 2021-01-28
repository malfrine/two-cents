from dataclasses import dataclass
from uuid import UUID

import pyomo.environ as pe

from pennies.model.user_personal_finances import UserPersonalFinances
from pennies.strategies.milp.sets import MILPSets


@dataclass
class MILPVariables:

    allocations: pe.Var
    balances: pe.Var
    paid_off_indicators: pe.Var

    @classmethod
    def create(
        cls, user_finances: UserPersonalFinances, sets: MILPSets
    ) -> "MILPVariables":

        allocations = pe.Var(
            sets.instruments,
            sets.months,
            bounds=(0.0, user_finances.financial_profile.monthly_allowance),
            initialize=user_finances.financial_profile.monthly_allowance,
        )
        balances = pe.Var(sets.instruments, sets.months, initialize=0)
        paid_off_indicators = pe.Var(
            sets.loans, sets.months, domain=pe.Binary, initialize=1
        )

        return MILPVariables(
            allocations=allocations,
            balances=balances,
            paid_off_indicators=paid_off_indicators,
        )

    def get_allocation(self, instrument: UUID, month: int):
        return self.allocations[instrument, month]

    def get_balance(self, instrument: UUID, month: int):
        return self.balances[instrument, month]

    def get_is_paid_off(self, loan: UUID, month: int):
        return self.paid_off_indicators[loan, month]
