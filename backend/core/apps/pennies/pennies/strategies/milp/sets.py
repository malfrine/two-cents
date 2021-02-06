from dataclasses import dataclass
from typing import List, ClassVar, Set
from uuid import UUID

import pyomo.environ as pe

from pennies.model.instrument import Instrument
from pennies.model.investment import Investment
from pennies.model.loan import Loan
from pennies.model.user_personal_finances import UserPersonalFinances


@dataclass
class MILPSets:
    instruments: Set
    months: Set
    investments: Set
    loans: Set

    @classmethod
    def from_user_finances(cls, user_finances: UserPersonalFinances) -> "MILPSets":
        instruments = set(i.name for i in user_finances.portfolio.instruments.values())
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
        months = set(range(user_finances.final_month))
        return MILPSets(
            instruments=instruments, investments=investments, loans=loans, months=months
        )
