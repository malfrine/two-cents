from typing import Dict, NewType

from pennies.model.processed.plan import ProcessedFinancialPlan

ProcessedSolution = NewType("ProcessedSolution", Dict[str, ProcessedFinancialPlan])
