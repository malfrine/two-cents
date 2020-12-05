from typing import List, Dict

import pandas as pd
from matplotlib import pyplot as plt

from pennies.model.solution import FinancialPlan


def _visualize_portfolios(portfolio_balances: List[Dict[str, float]]) -> None:
    ax = pd.DataFrame(portfolio_balances).plot(kind='bar',stacked=True, width=1.0, figsize=(10, 10))
    ax.set_xticks(range(0, 360, 10))
    plt.show()


def _visualize_payments(payments: List[Dict[str, float]]):
    ax = pd.DataFrame(payments).plot(kind='bar',stacked=True, width=1.0, figsize=(10, 10))
    ax.set_xticks(range(0, 360, 10))
    plt.show()


def visualize_solution(plan: FinancialPlan) -> None:
    starting_instruments = plan.monthly_solutions[0].portfolio.instruments
    portfolio_balances = [
        {name: ms.portfolio.get_instrument(name).current_balance if name in ms.portfolio.instruments else 0
         for name, _ in starting_instruments.items()}
        for ms in plan.monthly_solutions
    ]
    _visualize_portfolios(portfolio_balances)
    _visualize_payments([ms.allocation.payments for ms in plan.monthly_solutions])
