from typing import Union

from pydantic import BaseModel

from pennies.plan_processing.solution import ProcessedSolution
from pennies.model.status import PenniesStatus


class PenniesResponse(BaseModel):
    result: Union[ProcessedSolution, str]
    status: PenniesStatus
