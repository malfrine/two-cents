from rest_framework import serializers

from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.goals import FinancialGoal
from core.apps.finances.models.investments import Investment
from core.apps.finances.serializers.views.loan import LoanSerializer
from core.apps.payments.serializers import PaymentPlanSerializer
from core.apps.users.models import User


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        exclude = ("user",)


class FinancialGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        exclude = ("user",)


class FinancialProfileSerializer(serializers.ModelSerializer):
    # def validate(self, data):
    #     raise ValueError()

    class Meta:
        model = FinancialProfile
        exclude = ("user",)


class UserFinancesSerializer(serializers.ModelSerializer):

    loans = LoanSerializer(many=True, read_only=True)
    investments = InvestmentSerializer(many=True, read_only=True)
    goals = FinancialGoalSerializer(many=True, read_only=True)
    financial_profile = FinancialProfileSerializer(read_only=True)
    payment_plan = PaymentPlanSerializer(read_only=True)

    DICTIFY_FIELDS = ("loans", "investments", "goals")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in self.DICTIFY_FIELDS:
            rep[field] = {el["id"]: el for el in rep[field]}
        return rep

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "loans",
            "investments",
            "goals",
            "financial_profile",
            "payment_plan",
        )
