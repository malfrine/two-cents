from dataclasses import dataclass
from typing import List, Dict


@dataclass
class PaymentHorizon:
    order: int
    months: List[int]


@dataclass
class PaymentHorizons:
    data: List[PaymentHorizon]
    _month_to_horizon: Dict[int, PaymentHorizon] = None

    def corresponding_horizon(self, month: int) -> PaymentHorizon:
        if self._month_to_horizon is None:
            self._month_to_horizon = {m: ph for ph in self.data for m in ph.months}
        return self._month_to_horizon[month]


@dataclass
class PaymentHorizonsFactory:
    max_months: int = 3

    def from_num_months(self, start_month: int, final_month: int) -> PaymentHorizons:
        months = list(range(start_month, final_month))
        grouped_months = [
            months[i : i + self.max_months]
            for i in range(0, len(months), self.max_months)
        ]
        return PaymentHorizons(
            data=[
                PaymentHorizon(order=order, months=months)
                for order, months in enumerate(grouped_months)
            ]
        )
