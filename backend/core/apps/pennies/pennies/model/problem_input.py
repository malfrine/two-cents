from typing import List, Optional

from pydantic.main import BaseModel

from pennies.model.parameters import Parameters
from pennies.model.user_personal_finances import UserPersonalFinances


class ProblemInput(BaseModel):
    user_finances: UserPersonalFinances
    strategies: Optional[List[str]]
    parameters: Parameters = Parameters()
