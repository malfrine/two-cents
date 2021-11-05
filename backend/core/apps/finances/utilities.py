from datetime import date, datetime
from typing import Optional

from core.apps.payments.models import CurrentPaymentPlan, PlanType

MIN_PAYMENT_THRESHOLD = 10
BASIC_USER_LOAN_LIMIT = 3
BASIC_USER_INVESTMENT_LIMIT = 4
BASIC_USER_GOAL_LIMIT = 3


def calculate_months_between_dates(date1: date, date2: date):
    if date2 < date1:
        date1, date2 = date2, date1
    months = date2.month - date1.month + (12 * (date2.year - date1.year))
    return months


def get_first_date_of_next_month(d: Optional[date] = None):
    if d is None:
        d = datetime.today().date()
    if d.month == 12:
        return date(year=d.year + 1, month=1, day=1)
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


def can_create_loan(user):
    return _can_user_create(
        user.payment_plan, BASIC_USER_LOAN_LIMIT, len(user.loans.all())
    )


def can_create_goal(user):
    return _can_user_create(
        user.payment_plan, BASIC_USER_GOAL_LIMIT, len(user.goals.all())
    )


def can_create_investment(user):
    return _can_user_create(
        user.payment_plan, BASIC_USER_INVESTMENT_LIMIT, len(user.investments.all())
    )


def _can_user_create(
    payment_plan: CurrentPaymentPlan,
    max_items_allowed: int,
    current_number_of_items: int,
) -> bool:
    if payment_plan.plan_type == PlanType.LIMITED_FREE:
        if current_number_of_items >= max_items_allowed:
            return False
    return True
