from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from typing import Union, Dict, List
from functools import lru_cache


from dateutil.relativedelta import relativedelta

MONTHS_IN_YEAR = 12


@lru_cache
def get_first_date_of_next_month(dt: datetime) -> datetime:
    return (dt.replace(day=1) + timedelta(days=32)).replace(day=1)


@lru_cache
def get_months_difference(
    end: Union[datetime, date], start: Union[datetime, date]
) -> int:
    return (end.year - start.year) * 12 + end.month - start.month


@lru_cache
def get_date_plus_month(d: date, m: int) -> date:
    return d + relativedelta(months=m)


@dataclass
class DateTimeHelper:

    start_month: int
    max_month: int
    model_current_date: date
    month_ints_by_year: Dict[int, List[int]]

    def get_date_from_month_int(self, month: int) -> date:
        return get_date_plus_month(self.model_current_date, month)

    def get_month_int_from_date(self, d: date) -> int:
        return get_months_difference(d, self.model_current_date)

    @classmethod
    def create(
        cls, start_month: int, max_month: int, dt: datetime = None
    ) -> "DateTimeHelper":
        if dt is None:
            dt = datetime.today()
        model_current_date = get_first_date_of_next_month(dt)
        month_ints_by_year = defaultdict(list)
        for i in range(start_month, max_month):
            month_ints_by_year[get_date_plus_month(dt, i).year].append(i)
        return DateTimeHelper(
            start_month=start_month,
            max_month=max_month,
            model_current_date=model_current_date,
            month_ints_by_year=month_ints_by_year,
        )
