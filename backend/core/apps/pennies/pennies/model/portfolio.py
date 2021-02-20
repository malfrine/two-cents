from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel, validator, ValidationError

from pennies.model.instrument import Instrument
from pennies.model.investment import Investment, Cash
from pennies.model.loan import Loan
from pennies.utilities.dict import (
    get_value_from_dict,
)


class Portfolio(BaseModel):
    instruments: Dict[str, Instrument] = dict()

    @validator("instruments", pre=True)
    def list_to_dict(cls, v):
        if isinstance(v, list):
            return {i.name: i for i in v}
        elif isinstance(v, dict):
            return v
        else:
            raise ValidationError()

    @property
    def loans(self) -> List[Loan]:
        return list(l for l in self.instruments.values() if isinstance(l, Loan))

    @property
    def loans_by_id(self) -> Dict[UUID, Loan]:
        return {loan.id_: loan for loan in self.loans}

    @property
    def instruments_by_id(self) -> Dict[UUID, Instrument]:
        return {instrument.id_: instrument for instrument in self.instruments.values()}

    @property
    def investments_by_name(self) -> Dict[str, Investment]:
        # TODO: delete this and use id instead
        return {investment.name: investment for investment in self.investments()}

    def investments(self) -> List[Investment]:
        return list(i for i in self.instruments.values() if isinstance(i, Investment))

    @property
    def non_cash_investments(self) -> List[Investment]:
        return list(i for i in self.investments() if not isinstance(i, Cash))

    def get_loan(self, loan_name: str) -> Loan:
        return get_value_from_dict(loan_name, self.instruments)

    def get_investment(self, investment_name: str) -> Investment:
        return get_value_from_dict(investment_name, self.instruments)

    @property
    def final_month(self):
        return max((i.final_month or 0 for i in self.instruments.values()), default=0)

    def get_instrument(self, instrument_name: str) -> Instrument:
        return get_value_from_dict(instrument_name, self.instruments)

    def get_debt(self) -> float:
        return abs(sum(loan.current_balance for loan in self.loans))

    @property
    def net_worth(self) -> float:
        return sum(
            instrument.current_balance for instrument in self.instruments.values()
        )

    def __str__(self):
        return "\n\t".join(str(instrument) for instrument in self.instruments.values())
