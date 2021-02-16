from django.db import models
from core.apps.users.models import User as AuthUser
from core.utilities import get_current_age
from core.apps.finances.models.loans import Loan


class FinancialProfile(models.Model):
    user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, related_name="financial_profile"
    )
    birth_date = models.DateField(verbose_name="Birth Date")
    monthly_allowance = models.FloatField(verbose_name="Monthly Allowance")
    retirement_age = models.IntegerField(verbose_name="Retirement Age")
    risk_tolerance = models.FloatField(default=50.0, verbose_name="Risk Tolerance")
    # income
    # rrsp_contribution
    # rainy_day_fund_balance
    # tfsa contributions
    # TODO: add tax filing status

    @property
    def current_age(self):
        return get_current_age(self.birth_date)

    @property
    def years_to_retirement(self):
        return self.retirement_age - self.current_age

    @property
    def months_to_retirement(self):
        return self.years_to_retirement * 12

    def __str__(self):
        return "Profile" + " - " + str(self.user.pk)
