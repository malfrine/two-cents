from pydantic import BaseModel

from pennies.plan_processing.action_plan import ActionPlan
from pennies.plan_processing.failures import PlanFailures, PlanFailureType
from pennies.plan_processing.milestones import PlanMilestones
from pennies.plan_processing.net_worth_forecast import NetWorthForecast
from pennies.plan_processing.summaries import PlanSummaries


class ProcessedFinancialPlan(BaseModel):
    net_worth: NetWorthForecast
    summaries: PlanSummaries
    milestones: PlanMilestones
    action_plan: ActionPlan
    failures: PlanFailures

    @property
    def has_failed_goal(self) -> bool:
        for failure in self.failures:
            if failure.failure_type == PlanFailureType.UNSATISFIED_GOAL.value:
                return True
        return False
