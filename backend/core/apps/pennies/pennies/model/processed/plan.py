from pydantic import BaseModel

from pennies.model.processed.action_plan import ActionPlan
from pennies.model.processed.milestones import PlanMilestones
from pennies.model.processed.net_worth_forecast import NetWorthForecast
from pennies.model.processed.summaries import PlanSummaries


class ProcessedFinancialPlan(BaseModel):
    net_worth: NetWorthForecast
    summaries: PlanSummaries
    milestones: PlanMilestones
    action_plan: ActionPlan
