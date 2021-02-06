from rest_framework import serializers

from core.apps.finances.models.loans import LoanInterestTypes
from core.apps.users.models import User
from core.apps.finances.models.models import FinancialProfile, Investment
from core.apps.finances.models.models import Loan
from core.config import base


class LoanSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['interest_type'] == LoanInterestTypes.FIXED and not data['apr']:
            raise serializers.ValidationError("Fixed interest loans must have an APR")
        elif data['interest_type'] == LoanInterestTypes.VARIABLE and not data['prime_modifier']:
            raise serializers.ValidationError("Variable interest loans must have a Prime Modifier")
        return data

    class Meta:
        model = Loan
        exclude = ("user",)


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
            "prime_modifier",
            "minimum_monthly_payment",
            "final_month",
            "loan_type",
            "interest_type",
        )


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        exclude = ("user",)


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
        fields = (
            "name",
            "current_balance",
            "apr",
            "final_month",
            "minimum_monthly_payment",
        )


class PenniesFinancialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProfile
        fields = ("monthly_allowance", "years_to_retirement")


class UserFinancesSerializer(serializers.ModelSerializer):

    loans = LoanSerializer(many=True, read_only=True)
    investments = InvestmentSerializer(many=True, read_only=True)
    financial_profile = FinancialProfileSerializer(read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["loans"] = {loan["id"]: loan for loan in rep["loans"]}
        rep["investments"] = {loan["id"]: loan for loan in rep["investments"]}
        return rep

    class Meta:
        model = User
        fields = (
            "email",
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
    strategies = serializers.ReadOnlyField(
        default=["Two Cents Plan", "Avalanche Plan", "Snowball Plan"]
    )

    class Meta:
        model = User
        fields = ("loans", "investments", "financial_profile", "strategies")
        depth = 1
