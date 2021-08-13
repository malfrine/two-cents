from typing import Dict, NewType

from pennies.plan_processing.plan import ProcessedFinancialPlan

ProcessedSolution = NewType("ProcessedSolution", Dict[str, ProcessedFinancialPlan])
