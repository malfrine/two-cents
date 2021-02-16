from django.db import models


class InterestTypes(models.TextChoices):
    FIXED = "Fixed", "Fixed Interest Rate"
    VARIABLE = "Variable", "Variable Interest Rate"
