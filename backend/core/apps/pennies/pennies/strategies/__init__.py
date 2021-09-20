from enum import Enum

from pennies.strategies.allocation_strategy import PlanningStrategy
from pennies.strategies.greedy import (
    SnowballStrategy,
    AvalancheBallStrategy,
    AvalancheStrategy,
)
from pennies.strategies.milp.strategy import (
    MILPStrategy,
    InvestmentMILPStrategy,
    LoanMILPStrategy,
    GoalMILPStrategy,
)


class StrategyName(Enum):
    snowball = "Snowball Plan"
    avalanche = "Avalanche Plan"
    avalanche_ball = "Avalanche Ball Plan"
    two_cents_milp = "Two Cents Plan"
    investment_milp = "Investment-Focused Plan"
    loan_milp = "Loan-Focused Plan"
    goal_milp = "Goal-Focused Plan"


def get_strategy(strategy_name: str) -> PlanningStrategy:
    if strategy_name == StrategyName.snowball.value:
        return SnowballStrategy()
    elif strategy_name == StrategyName.avalanche.value:
        return AvalancheStrategy()
    elif strategy_name == StrategyName.avalanche_ball.value:
        return AvalancheBallStrategy()
    elif strategy_name == StrategyName.two_cents_milp.value:
        return MILPStrategy()
    elif strategy_name == StrategyName.investment_milp.investment_milp.value:
        return InvestmentMILPStrategy()
    elif strategy_name == StrategyName.loan_milp.value:
        return LoanMILPStrategy()
    elif strategy_name == StrategyName.goal_milp.value:
        return GoalMILPStrategy()
    else:
        raise NotImplementedError(
            f"Strategy {strategy_name} has not been implemented yet."
        )
