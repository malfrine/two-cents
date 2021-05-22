from django.contrib import admin
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.goals import FinancialGoal
from core.apps.finances.models.investments import Investment
from core.apps.finances.models.loans import Loan

# Register your models here.
admin.site.register(FinancialProfile)
admin.site.register(Loan)
admin.site.register(Investment)
admin.site.register(FinancialGoal)
