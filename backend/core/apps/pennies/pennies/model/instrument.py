from uuid import UUID, uuid4

from pydantic import Field
from pydantic.main import BaseModel

from pennies.model.interest_rate import InterestRate
from pennies.utilities.datetime import MONTHS_IN_YEAR


class Instrument(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    name: str
    interest_rate: InterestRate
    current_balance: float
    final_month: int = None

    def get_minimum_monthly_payment(self, month: int):
        raise NotImplementedError()

    def monthly_interest_rate(self, month: int) -> float:
        return self.interest_rate.get_monthly_interest_rate(month)

    def _add_to_current_balance(self, amount: float) -> None:
        self.current_balance += amount

    def _reduce_current_balance(self, amount) -> None:
        self.current_balance -= amount

    def incur_monthly_interest(self, month: int) -> None:
        self._add_to_current_balance(
            self.current_balance * self.monthly_interest_rate(month)
        )

    def receive_payment(self, payment) -> float:
        ...

    def get_type(self) -> str:
        ...

    def __str__(self):
        return "name: {}, type: {}, balance: ${:,.2f}, interest_rate: {:.2%}, term-length: {}".format(
            self.name,
            self.get_type(),
            self.current_balance,
            self.interest_rate.get_monthly_interest_rate(0),  # TODO: more descriptive
            "N/A" if self.final_month is None else self.final_month,
        )
