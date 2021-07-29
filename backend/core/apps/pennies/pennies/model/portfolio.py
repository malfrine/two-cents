from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel, validator, ValidationError

from pennies.model.constants import InvestmentAccountType
from pennies.model.instrument import Instrument
from pennies.model.interest_rate import ZeroGrowthRate
from pennies.model.investment import (
    Investment,
    Cash,
    GuaranteedInvestment,
    BaseInvestment,
)
from pennies.model.loan import Loan, Mortgage
from pennies.utilities.dict import get_value_from_dict


class Portfolio(BaseModel):
    instruments: Dict[UUID, Instrument] = dict()

    @validator("instruments", pre=True)
    def list_to_dict(cls, v):
        if isinstance(v, list):
            return {i.id_: i for i in v}
        elif isinstance(v, dict):
            return v
        else:
            raise ValidationError()

    @validator("instruments")
    def add_cash_account_if_needed(cls, v):
        for id_, instrument in v.items():
            if (
                isinstance(instrument, Cash)
                and instrument.account_type == InvestmentAccountType.NON_REGISTERED
            ):
                return v
        cash = Cash(
            db_id=-1,
            name="Generic Cash Account",
            interest_rate=ZeroGrowthRate(),
            current_balance=0,
            account_type=InvestmentAccountType.NON_REGISTERED,
            pre_authorized_monthly_contribution=0,
        )
        v[cash.id_] = cash
        return v

    @property
    def loans(self) -> List[Loan]:
        return list(l for l in self.instruments.values() if isinstance(l, Loan))

    @property
    def non_mortgage_loans(self) -> List[Loan]:
        return list(l for l in self.loans if not isinstance(l, Mortgage))

    @property
    def loans_by_id(self) -> Dict[UUID, Loan]:
        return {loan.id_: loan for loan in self.loans}

    @property
    def instruments_by_id(self) -> Dict[UUID, Instrument]:
        return {instrument.id_: instrument for instrument in self.instruments.values()}

    @property
    def rrsp_investments_and_guaranteed_investments(self) -> List[BaseInvestment]:
        return list(
            i
            for i in self.instruments.values()
            if isinstance(i, (Investment, GuaranteedInvestment))
            and i.account_type == InvestmentAccountType.RRSP
        )

    @property
    def non_tfsa_investments_and_guaranteed_investments(self) -> List[BaseInvestment]:
        return list(
            i
            for i in self.instruments.values()
            if isinstance(i, (Investment, GuaranteedInvestment))
            and i.account_type != InvestmentAccountType.TFSA
        )

    @property
    def investments_by_name(self) -> Dict[str, Investment]:
        # TODO: delete this and use id instead
        return {investment.id_: investment for investment in self.investments()}

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

    def get_instrument(self, id_: UUID) -> Instrument:
        return get_value_from_dict(id_, self.instruments)

    def get_debt(self) -> float:
        return abs(sum(loan.current_balance for loan in self.loans))

    @property
    def net_worth(self) -> float:
        return sum(
            instrument.current_balance for instrument in self.instruments.values()
        )

    def __str__(self):
        return "\n\t".join(str(instrument) for instrument in self.instruments.values())

    def get_investments_of_types(self, types: List):
        return list(i for i in self.investments() if isinstance(i, tuple(types)))

    @property
    def cash_investment(self):
        for investment in self.investments():
            if isinstance(investment, Cash):
                return investment
        raise ValueError("No cash investment exists")
