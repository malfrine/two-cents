from datetime import datetime, timedelta, date
from typing import Union

from dateutil.relativedelta import relativedelta


def get_first_date_of_next_month(dt: datetime) -> datetime:
    return (dt.replace(day=1) + timedelta(days=32)).replace(day=1)


def get_months_difference(
    end: Union[datetime, date], start: Union[datetime, date]
) -> int:
    return (end.year - start.year) * 12 + end.month - start.month


def get_date_plus_month(d: date, m: int) -> date:
    return d + relativedelta(months=m)
