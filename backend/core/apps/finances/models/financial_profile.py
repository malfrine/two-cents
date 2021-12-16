from datetime import datetime

from django.db import models

from core.apps.finances.models.financial_data import FinancialData
from core.apps.users.models import User as AuthUser
from core.utilities import get_current_age
from core.apps.finances.models.loans import Loan  # noqa

DEFAULT_BIRTH_DATE = datetime(year=1985, month=1, day=1).date()
DEFAULT_TAX_RATE = 0.3


class Province(models.TextChoices):
    AB = "AB", "Alberta"
    BC = "BC", "British Columbia"
    MB = "MB", "Manitoba"
    NB = "NB", "New Brunswick"
    NL = "NL", "Newfoundland and Labrador"
    NT = "NT", "Nunavut"
    ON = "ON", "Ontario"
    PEI = "PEI", "Prince Edward Island"
    QB = "QB", "Quebec"
    SK = "SK", "Saskatchewan"
    YK = "YK", "Yukon"


class FinancialProfileManager(models.Manager):
    def create_default(self, user: AuthUser):
        profile = self.model(financial_data=user.financial_data)
        profile.save()
        return profile


class FinancialProfile(models.Model):
    financial_data = models.OneToOneField(
        FinancialData, on_delete=models.CASCADE, related_name="financial_profile"
    )
    birth_date = models.DateField(default=DEFAULT_BIRTH_DATE, verbose_name="Birth Date")
    retirement_age = models.IntegerField(default=65, verbose_name="Retirement Age")
    risk_tolerance = models.FloatField(default=50.0, verbose_name="Risk Tolerance")
    monthly_salary_before_tax = models.FloatField(
        default=8000, verbose_name="Monthly Salary Before Tax"
    )
    percent_salary_for_spending = models.FloatField(
        default=25.0, verbose_name="Percent of Salary Allocated for Finances"
    )
    starting_rrsp_contribution_limit = models.FloatField(
        default=0, verbose_name="Remaining RRSP Contribution Limit"
    )
    starting_tfsa_contribution_limit = models.FloatField(
        default=0, verbose_name="Remaining TFSA Contribution Limit"
    )
    province_of_residence = models.CharField(
        max_length=50, choices=Province.choices, default=Province.AB,
    )
    death_age = models.IntegerField(default=90, verbose_name="Death Age")

    @property
    def current_age(self):
        return get_current_age(self.birth_date)

    @property
    def years_to_retirement(self):
        return self.retirement_age - self.current_age

    @property
    def years_to_death(self):
        return self.death_age - self.current_age

    @property
    def months_to_retirement(self):
        return self.years_to_retirement * 12

    @property
    def monthly_expenses_estimate(self):
        return (
            self.monthly_salary_before_tax
            * (1 - DEFAULT_TAX_RATE)
            * (1 - self.percent_salary_for_spending / 100)
        )

    def __str__(self):
        return "Profile" + " - " + str(self.financial_data.pk)

    objects = FinancialProfileManager()
