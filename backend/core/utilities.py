from datetime import date


def get_current_age(birth_date: date):
    todate = date.today()
    return (
        todate.year
        - birth_date.year
        - (todate.timetuple().tm_yday <= birth_date.timetuple().tm_yday)
    )


def get_months_between(start: date, end: date):
    return (end.year - start.year) * 12 + end.month - start.month
