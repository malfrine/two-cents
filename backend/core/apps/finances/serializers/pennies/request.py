from collections import defaultdict

from rest_framework import serializers

from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.investments import Investment
from core.apps.finances.models.loans import LoanType
from core.apps.finances.serializers.pennies.loan import LoanSerializer as PenniesLoanSerializer
from core.apps.users.models import User
from core.config import base


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
            "account_type"
        )


class PenniesFinancialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProfile
        fields = (
            "monthly_salary_before_tax",
            "years_to_retirement",
            "risk_tolerance",
            "percent_salary_for_spending",
            "province_of_residence",
            "starting_rrsp_contribution_limit",
            "starting_tfsa_contribution_limit",
            "current_age",
            "years_to_death"
        )


class PenniesRequestSerializer(base.ReadOnlyModelSerializer):
    loans = PenniesLoanSerializer(many=True, read_only=True)
    investments = PenniesInvestmentSerializer(many=True, read_only=True)
    financial_profile = PenniesFinancialProfileSerializer(read_only=True)
    strategies = serializers.ReadOnlyField(
        default=["Two Cents Plan", "Avalanche Plan", "Snowball Plan"]
    )

    def to_representation(self, instance):
        rep = super(PenniesRequestSerializer, self).to_representation(instance)
        # loans = rep.pop("loans", list())
        # loans_dict = defaultdict(list)
        # for loan in loans:
        #     loans_dict[loan["loan_type"]].append(loan)
        # rep["loans"] = loans_dict
        # TODO: group by loan type
        return rep


    class Meta:
        model = User
        fields = ("loans", "investments", "financial_profile", "strategies")
        depth = 1
