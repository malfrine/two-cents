from datetime import date, datetime
from rest_framework import serializers

from django.conf import settings
from core.apps.users.models import User
from core.apps.finances.models import FinancialProfile, Investment, Loan
from core.config import base
from core.utilities import get_current_age, get_months_between


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "name",
            "current_balance",
            "apr",
            "minimum_monthly_payment",
            "end_date",
        )


class PenniesLoanSerializer(serializers.ModelSerializer):


    current_balance = serializers.SerializerMethodField(source="get_current_balance")

    def get_current_balance(self, obj: Loan):
        return -obj.current_balance

    class Meta:
        model = Loan
        fields = (
            "name",
            "current_balance",
            "apr",
            "minimum_monthly_payment",
            "final_month",
        )


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ("name", "current_balance", "risk_level")


class FinancialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProfile
        fields = (
            "birth_date",
            "monthly_allowance",
            "retirement_age",
            "current_age",
            "years_to_retirement",
        )


class PenniesInvestmentSerializer(serializers.ModelSerializer):

    final_month = serializers.IntegerField(
        source="user.financial_profile.months_to_retirement", read_only=True
    )

    class Meta:
        model = Investment
        fields = ("name", "current_balance", "apr", "final_month", "minimum_monthly_payment")


class PenniesFinancialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProfile
        fields = ("monthly_allowance", "years_to_retirement")


class UserFinancesSerializer(serializers.ModelSerializer):

    loans = LoanSerializer(many=True, read_only=True)
    investments = InvestmentSerializer(many=True, read_only=True)
    financial_profile = FinancialProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "loans",
            "investments",
            "financial_profile",
        )


class PenniesRequestSerializer(base.ReadOnlyModelSerializer):
    loans = PenniesLoanSerializer(many=True, read_only=True)
    investments = PenniesInvestmentSerializer(many=True, read_only=True)
    financial_profile = PenniesFinancialProfileSerializer(read_only=True)
    strategies = serializers.ReadOnlyField(default=["linear-program", "avalanche"])

    class Meta:
        model = User
        fields = ("loans", "investments", "financial_profile", "strategies")
        depth = 1
