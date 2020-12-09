from rest_framework import serializers

from django.conf import settings
from core.apps.users.models import User
from core.apps.finances.models import FinancialProfile, Investment, Loan
from core.apps.users.serializers import UserSerializer

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ("name", "current_balance", "apr", "minimum_monthly_payment", "end_date")

class InvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ("name", "current_balance", "risk_level")


class FinancialProfileSerializer(serializers.ModelSerializer):

    def days_to_retirement(self, obj):
        return (obj.retirement_age - obj.birt_date).total_seconds() / 3600 / 24    
    
    class Meta:
        model = FinancialProfile
        fields = ("birth_date", "monthly_allowance", "retirement_age")

class UserFinancesSerializer(serializers.ModelSerializer):

    loans = LoanSerializer(many=True)
    investments = InvestmentSerializer(many=True)
    FinancialProfile = FinancialProfileSerializer()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "loans", "investments", "financial_profile")

    
    


