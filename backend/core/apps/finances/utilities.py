from datetime import date, datetime

MIN_PAYMENT_THRESHOLD = 10


def calculate_months_between_dates(date1: date, date2: date):
    if date2 < date1:
        date1, date2 = date2, date1
    months = date2.month - date1.month + (12 * (date2.year - date1.year))
    return months


def get_first_date_of_next_month():
    d = datetime.today().date()
    if d.month == 11:
        return date(year=d.year + 1, month=0, day=1)
    else:
        return date(year=d.year, month=d.month + 1, day=1)


def calculate_instalment_loan_min_payment(balance: float, apr: float, end_date: date):
    monthly_interest_rate = apr / 100 / 12
    months = calculate_months_between_dates(get_first_date_of_next_month(), end_date)
    if months == 0:
        return balance
    discount_factor = (
        monthly_interest_rate * (1 + monthly_interest_rate) ** months
    ) / ((1 + monthly_interest_rate) ** months - 1)
    min_payment = round(abs(balance) * discount_factor)
    return 0 if min_payment < MIN_PAYMENT_THRESHOLD else min_payment


def calculate_revolving_loan_min_payment(balance: float, apr: float):
    monthly_interest_rate = apr / 100 / 12
    min_payment = round(abs(balance) * monthly_interest_rate)
    return 0 if min_payment < MIN_PAYMENT_THRESHOLD else min_payment
