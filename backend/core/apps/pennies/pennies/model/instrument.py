from uuid import UUID, uuid4

from pydantic import Field
from pydantic.main import BaseModel


class Instrument(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    name: str
    apr: float
    current_balance: float
    minimum_monthly_payment: float
    final_month: int

    @property
    def monthly_interest_rate(self) -> float:
        return self.apr / 12 / 100

    def _add_to_current_balance(self, amount: float) -> None:
        self.current_balance += amount

    def _reduce_current_balance(self, amount) -> None:
        self.current_balance -= amount

    def incur_monthly_interest(self) -> None:
        self._add_to_current_balance(self.current_balance * self.monthly_interest_rate)

    def receive_payment(self, payment) -> float:
        ...

    def get_type(self) -> str:
        ...

    def __str__(self):
        return "name: {}, type: {}, balance: ${:,.2f}, interest_rate: {:.2%}, term-length: {}".format(
            self.name,
            self.get_type(),
            self.current_balance,
            self.apr / 100,
            self.final_month,
        )
