from enum import Enum

from pennies.strategies.allocation_strategy import AllocationStrategy
from pennies.strategies.greedy import SnowballStrategy, AvalancheBallStrategy, AvalancheStrategy
from pennies.strategies.lp import LinearProgramStrategy


class StrategyName(Enum):
    snowball = "snowball"
    avalanche = "avalanche"
    avalanche_ball = "avalanche-ball"
    lp = "linear-program"

def get_strategy(strategy_name: str) -> AllocationStrategy:
    if strategy_name == StrategyName.snowball.value:
        return SnowballStrategy()
    elif strategy_name == StrategyName.avalanche.value:
        return AvalancheStrategy()
    elif strategy_name == StrategyName.avalanche_ball.value:
        return AvalancheBallStrategy()
    elif strategy_name == StrategyName.lp.value:
        return LinearProgramStrategy()
    else:
        raise NotImplementedError(f"Strategy {strategy_name} has not been implemented yet.")
