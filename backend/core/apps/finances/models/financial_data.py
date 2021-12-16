from django.db import models

from core.apps.users.models import User as AuthUser


class FinancialData(models.Model):
    user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, related_name="financial_data"
    )
