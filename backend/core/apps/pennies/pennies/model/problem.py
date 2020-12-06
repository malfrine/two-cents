from pydantic import BaseModel

from pennies.model.portfolio import Portfolio
from pennies.model.request import PenniesRequest


class Problem(BaseModel):
    name: str = "portfolio"
    portfolio: Portfolio
    monthly_allowance: float

    def __str__(self):
        return (
            "name: {:s}, monthly_allowance ${:,.2f} \n".format(self.name, self.monthly_allowance)
            + "portfolio: \n\t{}".format(str(self.portfolio))
        )
