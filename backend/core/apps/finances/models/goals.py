from datetime import date

from django.db import models

from core.apps.finances.models.financial_data import FinancialData
from core.utilities import get_months_between


class GoalType(models.TextChoices):
    NEST_EGG = "Nest Egg", "Nest Egg"
    BIG_PURCHASE = "Big Purchase", "Big Purchase"


class FinancialGoal(models.Model):
    financial_data = models.ForeignKey(
        FinancialData, on_delete=models.CASCADE, related_name="goals"
    )
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=50, choices=GoalType.choices, default=GoalType.BIG_PURCHASE
    )
    amount = models.FloatField(
        default=None, blank=True, null=True, verbose_name="Amount to Save"
    )
    date = models.DateField(
        default=None, blank=True, null=True, verbose_name="Date to Completion"
    )

    @property
    def due_month(self):
        return get_months_between(date.today(), self.date)

    def __str__(self):
        return " - ".join(("Goal", str(self.pk), str(self.name)))
