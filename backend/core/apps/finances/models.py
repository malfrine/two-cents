from datetime import date
from enum import Enum
from django.db import models
from core.apps.users.models import User as AuthUser
from core.utilities import get_current_age, get_months_between


class Loan(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="loans")
    name = models.CharField(max_length=50)
    current_balance = models.FloatField(verbose_name="Current Balance")
    apr = models.FloatField(verbose_name="APR")
    minimum_monthly_payment = models.FloatField(verbose_name="Minimum Monthly Payment")
    end_date = models.DateField(null=False, verbose_name="Final Payment Month")

    @property
    def final_month(self):
        return get_months_between(date.today(), self.end_date)

    def __str__(self):
        return " - ".join(("Loan", str(self.pk), str(self.name)))


class Investment(models.Model):
    class RiskChoices(models.TextChoices):
        LOW = "Low", ("Low Risk")
        MEDIUM = "Medium", ("Medium Risk")
        HIGH = "High", "High Risk"

    _RISK_TO_APR = {
        RiskChoices.LOW: 3.0,
        RiskChoices.MEDIUM: 5.0,
        RiskChoices.HIGH: 7.0,
    }

    @property
    def apr(self):
        return self._RISK_TO_APR[self.risk_level]

    minimum_monthly_payment = 0

    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="investments"
    )
    name = models.CharField(max_length=50)
    current_balance = models.FloatField(verbose_name="Current Balance")
    risk_level = models.CharField(
        max_length=50,
        choices=RiskChoices.choices,
        default=RiskChoices.MEDIUM,
        verbose_name="Risk Type",
    )

    def __str__(self):
        return " - ".join(("Investment", str(self.pk), str(self.name)))


class FinancialProfile(models.Model):
    user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, related_name="financial_profile"
    )
    birth_date = models.DateField(verbose_name="Birth Date")
    monthly_allowance = models.FloatField(verbose_name="Monthly Allowance")
    retirement_age = models.IntegerField(verbose_name="Retirement Age")
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
