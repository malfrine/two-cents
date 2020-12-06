from django.db import models
from core.apps.users.models import User as AuthUser

# Create your models here.
LOAN_CHOICES = (("General", "General Loan"), )
INVESTMENT_CHOICES= (("General", "General Loan"), )

class Instrument(models.Model):
    name = models.CharField(max_length=50)
    apr = models.FloatField(verbose_name="APR")
    current_balance = models.FloatField(verbose_name="Current Balance")
    minimum_monthly_payment = models.FloatField(verbose_name="Minimum Monthly Payment")
    final_month = models.DateField(null=False, verbose_name="Final Payment Month")

    class Meta:
        abstract = True

class Loan(Instrument):
    loan_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=50, choices=LOAN_CHOICES, default="General", verbose_name="Loan Type")

    def __str__(self):
        return " - ".join(("Loan", str(self.loan_id), str(self.name)))

class Investment(Instrument):
    investment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    investment_type = models.CharField(
        max_length=50,
        choices=INVESTMENT_CHOICES,
        default="General",
        verbose_name="Investment Type"
    )

    def __str__(self):
        return " - ".join(("Investment", str(self.investment_id), str(self.name)))

class Profile(models.Model):
    user_id = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    monthly_allowance = models.FloatField(verbose_name="Monthly Allowance")

    def __str__(self):
        return "Profile" + " - " + str(self.user_id)
