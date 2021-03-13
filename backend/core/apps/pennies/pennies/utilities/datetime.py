from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from typing import Union, Dict, List

from dateutil.relativedelta import relativedelta


MONTHS_IN_YEAR = 12


def get_first_date_of_next_month(dt: datetime) -> datetime:
    return (dt.replace(day=1) + timedelta(days=32)).replace(day=1)


def get_months_difference(
    end: Union[datetime, date], start: Union[datetime, date]
) -> int:
    return (end.year - start.year) * 12 + end.month - start.month


def get_date_plus_month(d: date, m: int) -> date:
    return d + relativedelta(months=m)


@dataclass
class DateTimeHelper:

    model_current_date: date
    max_month: int

    def get_date_from_month_int(self, month: int) -> date:
        return get_date_plus_month(self.model_current_date, month)

    def get_month_int_from_date(self, d: date) -> int:
        return get_months_difference(d, self.model_current_date)

    @property
    def month_ints_by_year(self) -> Dict[int, List[int]]:
        d = defaultdict(list)
        for i in range(self.max_month):
            d[self.get_date_from_month_int(i).year].append(i)
        d = dict(d)
        return d

    @property
    def start_year(self):
        return self.model_current_date.year

    @classmethod
    def create(cls, max_month: int, dt: datetime = None) -> "DateTimeHelper":
        if dt is None:
            dt = datetime.today()
        model_current_date = get_first_date_of_next_month(dt)
        return DateTimeHelper(
            model_current_date=model_current_date, max_month=max_month
        )
