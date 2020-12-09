from django.contrib import admin
from core.apps.finances.models import FinancialProfile, Loan, Investment

# Register your models here.
admin.site.register(FinancialProfile)
admin.site.register(Loan)
admin.site.register(Investment)