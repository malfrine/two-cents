from dataclasses import dataclass
from typing import List, Dict, Tuple

from pennies.model.goal import BigPurchase, NestEgg
from pennies.model.user_personal_finances import UserPersonalFinances
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
    month_to_period_dict: Dict[int, DecisionPeriod] = None
    grouped_by_years: Dict[int, List[DecisionPeriod]] = None

    def __post_init__(self):
        self.month_to_period_dict = {m: ph for ph in self.data for m in ph.months}
        self.grouped_by_years = {
            year: [
                self.month_to_period_dict[month]
                for month in months
                if month in self.month_to_period_dict
            ]
            for year, months in self.dt_helper.month_ints_by_year.items()
        }

    def get_corresponding_period(self, month: int) -> DecisionPeriod:
        return self.month_to_period_dict[month]

    def get_decision_period_instances_in_year(self, year: int) -> List[DecisionPeriod]:
        """
        the number of times a decision period will show up in a year
        the length of this list should always be 12
        """
        return self.get_period_instances_in_months(self.get_months_in_year(year))

    def get_decision_period_indices(
        self, decision_periods: List[DecisionPeriod]
    ) -> List[int]:
        return [dp.index for dp in decision_periods]

    def get_indices_of_decision_period_instance_in_year(self, year: int) -> List[int]:
        decision_periods = self.get_decision_period_instances_in_year(year)
        return self.get_decision_period_indices(decision_periods)

    def get_period_instances_in_months(self, months: List[int]) -> List[DecisionPeriod]:
        return list(self.get_corresponding_period(month) for month in months)

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
    def max_month(self):
        return max(self.month_to_period_dict.keys())

    @property
    def min_month(self):
        return min(self.month_to_period_dict.keys())

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

    def get_months_in_year(self, year: int):
        return self.dt_helper.month_ints_by_year.get(year, list())


_Events = List[Tuple[int, bool]]
ACTION_PLAN_MONTHS = 3


def group_months(start: int, final: int, max_months: int) -> List[List[int]]:
    months = list(range(start, final))
    return [months[i : i + max_months] for i in range(0, len(months), max_months)]


def make_grouped_months_from_events(
    sorted_events: List[Tuple[int, bool]], max_months: int
) -> List[List[int]]:
    grouped_months = []
    for cur_event, next_event in zip(sorted_events, sorted_events[1:]):
        cur_month, is_cur_withdrawal = cur_event
        next_month, _ = next_event
        if is_cur_withdrawal:
            grouped_months.append([cur_month])
            cur_month += 1
            grouped_months.extend(group_months(cur_month, next_month, max_months))
        else:
            grouped_months.extend(group_months(cur_month, next_month, max_months))

    return grouped_months


def extract_major_events(
    user_finances: UserPersonalFinances, start_month: int
) -> Dict[int, bool]:
    withdrawal_events = {
        ACTION_PLAN_MONTHS: False,
        start_month: False,
        user_finances.financial_profile.retirement_month: False,
        user_finances.financial_profile.death_month: False,
    }
    for goal in user_finances.goals.values():
        if isinstance(goal, BigPurchase):
            withdrawal_events[goal.due_month] = True
        elif isinstance(goal, NestEgg):
            if goal.due_month not in withdrawal_events.keys():
                withdrawal_events[goal.due_month] = False
    for loan in user_finances.portfolio.loans:
        if loan.final_month is None:
            continue
        elif loan.final_month not in withdrawal_events.keys():
            withdrawal_events[loan.final_month] = False
    return withdrawal_events


def make_sorted_events(
    user_finances: UserPersonalFinances, start_month: int
) -> Tuple[_Events, _Events]:
    major_events = extract_major_events(user_finances, start_month)
    sorted_events = sorted(major_events.items(), key=lambda x: x[0])
    sorted_events = [
        (month, is_withdrawal)
        for month, is_withdrawal in sorted_events
        if month >= start_month
    ]
    retirement_month = user_finances.financial_profile.retirement_month
    working_events = [
        (month, is_withdrawal)
        for month, is_withdrawal in sorted_events
        if month <= retirement_month
    ]
    retirement_events = [
        (month, is_withdrawal)
        for month, is_withdrawal in sorted_events
        if month >= retirement_month
    ]
    return working_events, retirement_events


@dataclass
class DecisionPeriodsManagerFactory:
    max_working_months: int = 12
    max_retirement_months: int = 12

    def from_num_months(
        self, start_month: int, retirement_month: int, final_month: int
    ) -> DecisionPeriodsManager:
        cur_index = 0
        data = list()
        for grouped_months in group_months(
            start_month, retirement_month, self.max_working_months
        ):
            data.append(WorkingPeriod(index=cur_index, months=grouped_months))
            cur_index += 1
        for grouped_months in group_months(
            retirement_month, final_month, self.max_retirement_months
        ):
            data.append(RetirementPeriod(index=cur_index, months=grouped_months))
            cur_index += 1
        dt_helper = DateTimeHelper.create(start_month, final_month)
        return DecisionPeriodsManager(data=data, dt_helper=dt_helper)

    def from_user_finances(
        self, start_month: int, user_finances: UserPersonalFinances
    ) -> DecisionPeriodsManager:
        working_events, retirement_events = make_sorted_events(
            user_finances, start_month
        )
        grouped_working_months = make_grouped_months_from_events(
            working_events, self.max_working_months
        )
        grouped_retirement_months = make_grouped_months_from_events(
            retirement_events, self.max_retirement_months
        )
        data = list()
        cur_index = 0
        for working_months in grouped_working_months:
            data.append(WorkingPeriod(index=cur_index, months=working_months))
            cur_index += 1
        for retirement_months in grouped_retirement_months:
            data.append(RetirementPeriod(index=cur_index, months=retirement_months))
            cur_index += 1
        dt_helper = DateTimeHelper.create(
            start_month, user_finances.financial_profile.death_month
        )
        return DecisionPeriodsManager(data=data, dt_helper=dt_helper)
