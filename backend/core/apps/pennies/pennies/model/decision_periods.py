from dataclasses import dataclass
from typing import List, Dict

from pennies.utilities.datetime import DateTimeHelper


@dataclass
class DecisionPeriod:
    index: int
    months: List[int]


class WorkingPeriod(DecisionPeriod):
    pass


class RetirementPeriod(DecisionPeriod):
    pass


@dataclass
class DecisionPeriodsManager:
    data: List[DecisionPeriod]
    dt_helper: DateTimeHelper
    _month_to_period: Dict[int, DecisionPeriod] = None
    _grouped_by_years: Dict[int, List[DecisionPeriod]] = None

    def get_corresponding_period(self, month: int) -> DecisionPeriod:
        return self.month_to_period_dict[month]

    def get_corresponding_period_or_closest(self, month: int) -> DecisionPeriod:
        """If the corresponding period for a month doesn't exist - the closes one will be selected"""
        if month < self.min_month:
            return self.data[self.min_period_index]
        elif month > self.max_month:
            return self.data[self.max_period_index]
        else:
            return self.get_corresponding_period(month)

    @property
    def all_periods(self) -> List[DecisionPeriod]:
        return self.data

    @property
    def max_period_index(self) -> int:
        return max(dp.index for dp in self.all_periods)

    @property
    def min_period_index(self) -> int:
        return min(dp.index for dp in self.all_periods)

    @property
    def working_periods(self) -> List[WorkingPeriod]:
        return list(
            period for period in self.all_periods if isinstance(period, WorkingPeriod)
        )

    @property
    def retirement_periods(self) -> List[RetirementPeriod]:
        return list(
            period
            for period in self.all_periods
            if isinstance(period, RetirementPeriod)
        )

    @property
    def month_to_period_dict(self):
        if self._month_to_period is None:
            self._month_to_period = {m: ph for ph in self.data for m in ph.months}
        return self._month_to_period

    @property
    def max_month(self):
        return max(self.month_to_period_dict.keys())

    @property
    def min_month(self):
        return min(self.month_to_period_dict.keys())

    @property
    def grouped_by_years(self) -> Dict[int, List[DecisionPeriod]]:
        if not self._grouped_by_years:
            self._grouped_by_years = {
                year: [
                    self.month_to_period_dict[month]
                    for month in months
                    if month in self.month_to_period_dict
                ]
                for year, months in self.dt_helper.month_ints_by_year.items()
            }
        return self._grouped_by_years

    def get_years_in_decision_period(self, dp_index: int) -> List[int]:
        return list(
            set(
                self.dt_helper.get_date_from_month_int(month).year
                for month in self.data[dp_index].months
            )
        )

    def get_decision_periods_after_month(self, due_month) -> List[int]:
        first_period = self.get_corresponding_period_or_closest(due_month)
        return list(
            wp.index for wp in self.all_periods if wp.index >= first_period.index
        )


@dataclass
class DecisionPeriodsManagerFactory:
    max_months: int = 3

    def from_num_months(
        self, start_month: int, retirement_month: int, final_month: int
    ) -> DecisionPeriodsManager:
        cur_index = 0
        data = list()
        for grouped_months in self._group_months(start_month, retirement_month):
            data.append(WorkingPeriod(index=cur_index, months=grouped_months))
            cur_index += 1
        for grouped_months in self._group_months(retirement_month, final_month):
            data.append(RetirementPeriod(index=cur_index, months=grouped_months))
            cur_index += 1
        dt_helper = DateTimeHelper.create(final_month)
        return DecisionPeriodsManager(data=data, dt_helper=dt_helper)

    def _group_months(self, start: int, final: int) -> List[List[int]]:
        months = list(range(start, final))
        return [
            months[i : i + self.max_months]
            for i in range(0, len(months), self.max_months)
        ]
