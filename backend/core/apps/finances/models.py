from django.db import models
from core.apps.users.models import User as AuthUser

RISK_CHOICES = (
        ("Low", "Low Risk"), 
        ("Medium", "Medium Risk"),
        ("High", "High Risk"),
    )

class Loan(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="loans")
    name = models.CharField(max_length=50)
    current_balance = models.FloatField(verbose_name="Current Balance")
    apr = models.FloatField(verbose_name="APR")
    minimum_monthly_payment = models.FloatField(verbose_name="Minimum Monthly Payment")
    end_date = models.DateField(null=False, verbose_name="Final Payment Month")

    def __str__(self):
        return " - ".join(("Loan", str(self.pk), str(self.name)))

class Investment(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="investments")
    name = models.CharField(max_length=50)
    current_balance = models.FloatField(verbose_name="Current Balance")
    risk_level = models.CharField(max_length=50, choices=RISK_CHOICES, default="General", verbose_name="Risk Type")

    def __str__(self):
        return " - ".join(("Investment", str(self.pk), str(self.name)))

class FinancialProfile(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="financial_profile", unique=True)
    birth_date = models.DateField(verbose_name="Birth Date")
    monthly_allowance = models.FloatField(verbose_name="Monthly Allowance")
    retirement_age = models.IntegerField(verbose_name="Retirement Age")
    
    def __str__(self):
        return "Profile" + " - " + str(self.user.pk)
