from typing import List, Dict

import pandas as pd
from matplotlib import pyplot as plt

from pennies.model.solution import FinancialPlan


def _visualize_portfolios(portfolio_balances: List[Dict[str, float]], suffix) -> None:
    ax = pd.DataFrame(portfolio_balances).plot(
        kind="bar", stacked=True, width=1.0, figsize=(10, 10)
    )
    ax.set_xticks(range(0, len(portfolio_balances), 24))
    plt.savefig(f"portfolio-{suffix}.png")


def _visualize_money_movements(money_movements: List[Dict[str, float]], suffix):
    df = pd.DataFrame(money_movements)
    ax = df.plot(kind="bar", stacked=True, width=1.0, figsize=(10, 10))
    ax.set_xticks(range(0, len(money_movements), 24))
    plt.savefig(f"payments-{suffix}.png")


def visualize_solution(plan: FinancialPlan, suffix="") -> None:
    starting_instruments = plan.monthly_solutions[0].portfolio.instruments
    portfolio_balances = [
        {
            instrument.name: ms.portfolio.get_instrument(id_).current_balance
            if id_ in ms.portfolio.instruments.keys()
            else 0
            for id_, instrument in starting_instruments.items()
        }
        for ms in plan.monthly_solutions
    ]
    money_movements = list()
    for ms in plan.monthly_solutions:
        money_movement = {
            instrument.name: -ms.allocation.payments.get(id_, 0)
            + ms.withdrawals.get(id_, 0)
            for id_, instrument in starting_instruments.items()
        }
        money_movements.append(money_movement)
    _visualize_money_movements(money_movements, suffix=suffix)
    _visualize_portfolios(portfolio_balances, suffix=suffix)
