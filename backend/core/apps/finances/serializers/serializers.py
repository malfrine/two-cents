from rest_framework import serializers

from core.apps.finances.models.financial_data import FinancialData
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.goals import FinancialGoal
from core.apps.finances.models.investments import Investment
from core.apps.finances.serializers.views.loan import LoanSerializer
from core.apps.payments.serializers import PaymentPlanSerializer
from core.apps.users.models import User


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        exclude = ("financial_data",)


class FinancialGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        exclude = ("financial_data",)


class FinancialProfileSerializer(serializers.ModelSerializer):
    # def validate(self, data):
    #     raise ValueError()

    class Meta:
        model = FinancialProfile
        exclude = ("financial_data",)


class FinancialDataSerializer(serializers.ModelSerializer):

    loans = LoanSerializer(many=True, read_only=True)
    investments = InvestmentSerializer(many=True, read_only=True)
    goals = FinancialGoalSerializer(many=True, read_only=True)
    financial_profile = FinancialProfileSerializer(read_only=True)

    DICTIFY_FIELDS = ("loans", "investments", "goals")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in self.DICTIFY_FIELDS:
            rep[field] = {el["id"]: el for el in rep[field]}
        return rep

    class Meta:
        model = FinancialData
        fields = "__all__"


class UserFinancesSerializer(serializers.ModelSerializer):

    financial_data = FinancialDataSerializer(read_only=True)
    payment_plan = PaymentPlanSerializer(read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        financial_data = rep.get("financial_data", dict())
        # TODO: update how the data is processed on the FE so we don't have to add financial data fields
        for field in financial_data:
            rep[field] = financial_data[field]
        return rep

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "financial_data",
            "payment_plan",
            "is_admin",
            "is_staff",
            "is_active",
        )
