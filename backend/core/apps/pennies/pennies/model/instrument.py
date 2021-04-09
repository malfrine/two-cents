from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field
from pydantic.main import BaseModel

from pennies.model.interest_rate import CompoundingRate
from pennies.utilities.datetime import MONTHS_IN_YEAR


class Instrument(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    name: str
    interest_rate: CompoundingRate
    current_balance: float = None
    final_month: int = None

    @property
    def volatility(self):
        return self.interest_rate.get_volatility()

    @property
    def volatility_fraction(self):
        return self.volatility / 100 / MONTHS_IN_YEAR

    def get_minimum_monthly_payment(self, month: int):
        raise NotImplementedError()

    def get_maximum_monthly_payment(self, month: int) -> Optional[float]:
        return None

    def monthly_interest_rate(self, month: int) -> float:
        return self.interest_rate.get_monthly_interest_rate(month)

    def get_type(self) -> str:
        ...

    def __str__(self):
        return "name: {}, type: {}, balance: ${:,.2f}, interest_rate: {:.2%}, term-length: {}".format(
            self.name,
            self.get_type(),
            self.current_balance or 0,
            self.interest_rate.get_monthly_interest_rate(0),  # TODO: more descriptive
            "N/A" if self.final_month is None else self.final_month,
        )

    # class Meta:
    #     underscore_attrs_are_private = True
