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
    MORTGAGE = "Mortgage", "Mortgage"


INSTALMENT_LOANS = [LoanType.PERSONAL_LOAN, LoanType.STUDENT_LOAN, LoanType.CAR_LOAN]
REVOLVING_LOANS = [
    LoanType.CREDIT_CARD,
    LoanType.LINE_OF_CREDIT,
    LoanType.STUDENT_LINE_OF_CREDIT,
]


def get_required_fields_map():
    all_loan_fields = ["name", "current_balance", "loan_type", "interest_type"]
    instalment_loans = all_loan_fields + ["end_date", "minimum_monthly_payment"]
    revolving_loans = all_loan_fields
    mortgage_loans = [
        "name",
        "monthly_payment",
        "purchase_price",
        "purchase_date",
        "downpayment_amount",
        "amortization_years",
        "current_term_start_date",
        "current_term_end_date",
        "interest_type"
    ]
    return {
        LoanType.CREDIT_CARD: revolving_loans,
        LoanType.LINE_OF_CREDIT: revolving_loans,
        LoanType.STUDENT_LINE_OF_CREDIT: revolving_loans,
        LoanType.PERSONAL_LOAN: instalment_loans,
        LoanType.STUDENT_LOAN: instalment_loans,
        LoanType.CAR_LOAN: instalment_loans,
        LoanType.MORTGAGE: mortgage_loans
    }


LOAN_REQUIRED_FIELDS_MAP = get_required_fields_map()


def get_loan_interest_required_fields_map():
    return {
        InterestTypes.FIXED: "apr",
        InterestTypes.VARIABLE: "prime_modifier"
    }


LOAN_INTEREST_REQUIRED_FIELDS_MAP = get_loan_interest_required_fields_map()


class LoanInterest(models.Model):
    interest_type = models.CharField(
        max_length=50,
        choices=InterestTypes.choices,
        default=InterestTypes.FIXED,
    )
    apr = models.FloatField(default=None, blank=True, null=True, verbose_name="APR")
    prime_modifier = models.FloatField(
        default=None, blank=True, null=True, verbose_name="Prime Modifier"
    )


class MortgageDetails(models.Model):
    monthly_payment = models.FloatField(verbose_name="Monthly Payment")
    purchase_price = models.FloatField(verbose_name="House Purchase Price")
    purchase_date = models.DateField(verbose_name="Purchase Date")
    downpayment_amount = models.FloatField(verbose_name="Downpayment")
    amortization_years = models.FloatField(verbose_name="Amortization Period in Years")
    current_term_start_date = models.DateField(verbose_name="Current Term Start Date")
    current_term_years = models.FloatField(verbose_name="Current Term Length in Years")


class Loan(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="loans")
    name = models.CharField(max_length=50)
    loan_type = models.CharField(
        max_length=50, choices=LoanType.choices, default=LoanType.PERSONAL_LOAN
    )

    loan_interest = models.OneToOneField(LoanInterest, on_delete=models.CASCADE, related_name="loan_interest")
    current_balance = models.FloatField(default=None, blank=True, null=True, verbose_name="Current Balance")

    minimum_monthly_payment = models.FloatField(
        default=None, blank=True, null=True, verbose_name="Minimum Monthly Payment"
    )
    end_date = models.DateField(
        default=None, blank=True, null=True, verbose_name="Final Payment Month"
    )

    mortgage_details = models.OneToOneField(MortgageDetails, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name="mortgage_details")

    @property
    def final_month(self):
        if self.end_date is None:
            return None
        else:
            return get_months_between(date.today(), self.end_date)

    def __str__(self):
        return " - ".join(("Loan", str(self.pk), str(self.name)))

    @classmethod
    def is_instalment_loan(cls, loan_type: LoanType):
        return loan_type in INSTALMENT_LOANS




