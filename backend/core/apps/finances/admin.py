from django.contrib import admin
from core.apps.finances.models.models import FinancialProfile, Investment
from core.apps.finances.models.loans import Loan

# Register your models here.
admin.site.register(FinancialProfile)
admin.site.register(Loan)
admin.site.register(Investment)
