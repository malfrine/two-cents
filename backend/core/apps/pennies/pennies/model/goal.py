from typing import Literal, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from pennies.model.investment import (
    Cash,
    ALL_NON_GUARANTEED_INVESTMENTS,
)


class BaseFinancialGoal(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    name: str
    amount: float
    due_month: int

    def get_allowed_accounts(self):
        return ALL_NON_GUARANTEED_INVESTMENTS


class BaseSavingsGoal(BaseFinancialGoal):
    """A type of goal with which the user just wants to make sure that the balance of certain set of accounts is met"""

    pass


class BasePurchaseGoal(BaseFinancialGoal):
    """A type of goal with which the user wants to withdraw a set amount of money from their accounts"""

    pass


class NestEgg(BaseSavingsGoal):
    type: Literal["Nest Egg"] = "Nest Egg"

    def get_allowed_accounts(self):
        return [Cash]


class BigPurchase(BasePurchaseGoal):
    type: Literal["Big Purchase"] = "Big Purchase"


AllGoalTypes = Union[NestEgg, BigPurchase]
