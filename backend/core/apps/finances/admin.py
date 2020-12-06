from django.contrib import admin
from core.apps.finances.models import Profile, Loan, Investment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Loan)
admin.site.register(Investment)