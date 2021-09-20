from rest_framework import serializers

from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.goals import FinancialGoal
from core.apps.finances.models.investments import Investment, InvestmentType
from core.apps.finances.serializers.pennies.loan import (
    LoanSerializer as PenniesLoanSerializer,
)
from core.apps.users.models import User
from core.config import base
from core.config.base import drop_none_fields


class PenniesInvestmentSerializer(serializers.ModelSerializer):

    db_id = serializers.SerializerMethodField(source="get_db_id")

    def get_db_id(self, obj: Investment):
        return obj.pk

    def to_representation(self, instance):
        rep = super(PenniesInvestmentSerializer, self).to_representation(instance)
        investment_type = InvestmentType(rep.get("investment_type"))
        if investment_type in (InvestmentType.GIC, InvestmentType.TERM_DEPOSIT):
            # guaranteed investment
            interest_rate = {
                "interest_type": "Guaranteed Investment Return Rate",
                "interest_rate": {
                    "interest_type": f"{rep.pop('interest_type')} Investment Return Rate",
                    "roi": rep.pop("roi"),
                    "volatility": rep.pop("volatility"),
                    "prime_modifier": rep.pop("prime_modifier"),
                },
                "final_month": rep.get("final_month"),
            }
        elif investment_type == InvestmentType.CASH:
            rep.pop("interest_type")
            interest_rate = {
                "interest_type": "Zero Growth",
            }
        else:
            rep.pop("interest_type")
            interest_rate = {
                "interest_type": "Investment Return Rate",
                "roi": rep.pop("roi"),
                "volatility": rep.pop("volatility"),
            }
        interest_rate = drop_none_fields(interest_rate)
        rep["interest_rate"] = interest_rate
        print(rep)
        return rep

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
            "account_type",
            "db_id",
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
            "years_to_death",
        )


class PenniesFinancialGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = ("name", "type", "amount", "due_month")


class PenniesRequestSerializer(base.ReadOnlyModelSerializer):
    loans = PenniesLoanSerializer(many=True, read_only=True)
    investments = PenniesInvestmentSerializer(many=True, read_only=True)
    goals = PenniesFinancialGoalSerializer(many=True, read_only=True)
    financial_profile = PenniesFinancialProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "loans",
            "investments",
            "goals",
            "financial_profile",
        )
        depth = 1
