from enum import Enum

from pennies.strategies.allocation_strategy import AllocationStrategy
from pennies.strategies.greedy import (
    SnowballStrategy,
    AvalancheBallStrategy,
    AvalancheStrategy,
)
from pennies.strategies.milp.strategy import MILPStrategy


class StrategyName(Enum):
    snowball = "Snowball Plan"
    avalanche = "Avalanche Plan"
    avalanche_ball = "Avalanche Ball Plan"
    lp = "Two Cents Plan"


def get_strategy(strategy_name: str) -> AllocationStrategy:
    if strategy_name == StrategyName.snowball.value:
        return SnowballStrategy()
    elif strategy_name == StrategyName.avalanche.value:
        return AvalancheStrategy()
    elif strategy_name == StrategyName.avalanche_ball.value:
        return AvalancheBallStrategy()
    elif strategy_name == StrategyName.lp.value:
        return MILPStrategy()
    else:
        raise NotImplementedError(
            f"Strategy {strategy_name} has not been implemented yet."
        )
