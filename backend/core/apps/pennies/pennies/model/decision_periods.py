from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DecisionPeriod:
    index: int
    months: List[int]


class WorkingPeriod(DecisionPeriod):
    pass


class RetirementPeriod(DecisionPeriod):
    pass


@dataclass
class DecisionPeriods:
    data: List[DecisionPeriod]
    _month_to_period: Dict[int, DecisionPeriod] = None

    def corresponding_horizon(self, month: int) -> DecisionPeriod:
        if self._month_to_period is None:
            self._month_to_period = {m: ph for ph in self.data for m in ph.months}
        return self._month_to_period[month]

    @property
    def all_periods(self) -> List[DecisionPeriod]:
        return self.data

    @property
    def working_periods(self) -> List[WorkingPeriod]:
        return list(period for period in self.all_periods if isinstance(period, WorkingPeriod))

    @property
    def retirement_periods(self) -> List[RetirementPeriod]:
        return list(period for period in self.all_periods if isinstance(period, RetirementPeriod))


@dataclass
class DecisionPeriodsFactory:
    max_months: int = 3

    def from_num_months(self, start_month: int, retirement_month: int, final_month: int) -> DecisionPeriods:
        cur_index = 0
        data = list()
        for grouped_months in self._group_months(start_month, retirement_month):
            data.append(WorkingPeriod(index=cur_index, months=grouped_months))
            cur_index += 1
        for grouped_months in self._group_months(retirement_month, final_month):
            data.append(RetirementPeriod(index=cur_index, months=grouped_months))
            cur_index += 1
        return DecisionPeriods(data=data)

    def _group_months(self, start: int, final: int) -> List[List[int]]:
        months = list(range(start, final))
        return [
            months[i : i + self.max_months]
            for i in range(0, len(months), self.max_months)
        ]
