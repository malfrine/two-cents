from datetime import date

from django.db import models

from core.apps.finances.models.constants import InterestTypes
from core.apps.users.models import User as AuthUser
from core.utilities import get_months_between


class LoanType(models.TextChoices):
    CREDIT_CARD = "Credit Card", "Credit Card Loan"
    LINE_OF_CREDIT = "Line of Credit", "Line Of Credit"
    STUDENT_LOAN = "Student Loan", "Student Loan"
    STUDENT_LINE_OF_CREDIT = "Student Line of Credit", "Student Line of Credit"
    PERSONAL_LOAN = "Personal Loan", "Personal Loan"
    CAR_LOAN = "Car Loan", "Car Loan"


INSTALMENT_LOANS = [LoanType.PERSONAL_LOAN, LoanType.STUDENT_LOAN, LoanType.CAR_LOAN]
REVOLVING_LOANS = [
    LoanType.CREDIT_CARD,
    LoanType.LINE_OF_CREDIT,
    LoanType.STUDENT_LINE_OF_CREDIT,
]


class Loan(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="loans")
    name = models.CharField(max_length=50)
    current_balance = models.FloatField(verbose_name="Current Balance")
    apr = models.FloatField(default=None, blank=True, null=True, verbose_name="APR")
    prime_modifier = models.FloatField(
        default=None, blank=True, null=True, verbose_name="Prime Modifier"
    )
    minimum_monthly_payment = models.FloatField(default=None, blank=True, null=True, verbose_name="Minimum Monthly Payment")
    end_date = models.DateField(
        default=None, blank=True, null=True, verbose_name="Final Payment Month"
    )
    interest_type = models.CharField(
        max_length=50,
        choices=InterestTypes.choices,
        default=InterestTypes.FIXED,
    )
    loan_type = models.CharField(
        max_length=50, choices=LoanType.choices, default=LoanType.PERSONAL_LOAN
    )

    @property
    def final_month(self):
        if self.end_date is None:
            return None
        else:
            return get_months_between(date.today(), self.end_date)

    def __str__(self):
        return " - ".join(("Loan", str(self.pk), str(self.name)))
