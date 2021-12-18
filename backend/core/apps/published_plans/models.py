from django.db import models

from core.apps.finances.models.financial_data import FinancialData


class PublishedPlan(models.Model):
    financial_data = models.OneToOneField(FinancialData, on_delete=models.CASCADE)
