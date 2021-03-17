from rest_framework import serializers

from core.apps.finances.models.constants import InterestTypes
from core.apps.users.models import User
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.investments import Investment
from core.apps.finances.models.financial_profile import Loan
from core.config import base


class LoanSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["interest_type"] == InterestTypes.FIXED and not data["apr"]:
            raise serializers.ValidationError("Fixed interest loans must have an APR")
        elif (
            data["interest_type"] == InterestTypes.VARIABLE
            and not data["prime_modifier"]
        ):
            raise serializers.ValidationError(
                "Variable interest loans must have a Prime Modifier"
            )
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

    # def validate(self, data):
    #     raise ValueError()

    class Meta:
        model = FinancialProfile
        fields = (
            "birth_date",
            "monthly_allowance",
            "retirement_age",
            "current_age",
            "years_to_retirement",
            "risk_tolerance",
        )


class PenniesInvestmentSerializer(serializers.ModelSerializer):

    # final_month = serializers.IntegerField(
    #     source="user.financial_profile.months_to_retirement", read_only=True
    # )

    class Meta:
        model = Investment
        fields = (
            "name",
            "current_balance",
            "roi",
            "final_month",
            "volatility",
            "investment_type",
            "pre_authorized_monthly_contribution",
            "principal_investment_amount",
            "start_month",
            "prime_modifier",
            "interest_type",
        )


class PenniesFinancialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProfile
        fields = ("monthly_allowance_before_retirement", "years_to_retirement", "risk_tolerance")


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
