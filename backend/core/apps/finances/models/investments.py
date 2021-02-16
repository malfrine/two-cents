from django.db import models

from core.apps.users.models import User as AuthUser


class InvestmentType(models.TextChoices):
    MUTUAL_FUND = "Mutual Fund", "Mutual Fund"
    ETF = "ETF", "Exchange Traded Fund"
    GIC = "GIC", "Guaranteed Investment Certificate"
    TERM_DEPOSIT = "Term Deposit", "Term Deposit"
    STOCK = "Stock", "Stock"


class RiskChoices(models.TextChoices):
    LOW = "Low", "Low Risk"
    MEDIUM = "Medium", "Medium Risk"
    HIGH = "High", "High Risk"


class Investment(models.Model):

    _RISK_TO_APR = {
        RiskChoices.LOW: 3.5,
        RiskChoices.MEDIUM: 5.0,
        RiskChoices.HIGH: 7.0,
    }

    _RISK_TO_VOLATILITY = {
        RiskChoices.LOW: 1.5,
        RiskChoices.MEDIUM: 3.5,
        RiskChoices.HIGH: 7.5,
    }

    @property
    def apr(self):
        return self._RISK_TO_APR[self.risk_level]

    @property
    def volatility(self):
        return self._RISK_TO_VOLATILITY[self.risk_level]

    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="investments"
    )
    name = models.CharField(max_length=50)
    current_balance = models.FloatField(verbose_name="Current Balance")
    minimum_monthly_payment = models.FloatField(
        default=0, verbose_name="Minimum Monthly Payment"
    )
    current_monthly_contribution = models.FloatField(
        default=0, verbose_name="Current Monthly Payment"
    )
    risk_level = models.CharField(
        max_length=50,
        choices=RiskChoices.choices,
        default=RiskChoices.MEDIUM,
        verbose_name="Risk Type",
    )

    def __str__(self):
        return " - ".join(("Investment", str(self.pk), str(self.name)))
