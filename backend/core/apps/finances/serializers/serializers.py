from rest_framework import serializers

from core.apps.finances.serializers.views.loan import LoanSerializer
from core.apps.users.models import User
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.investments import Investment


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        exclude = ("user",)


# class MortgageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Mortgage
#         exclude = ("user",)


class FinancialProfileSerializer(serializers.ModelSerializer):
    # def validate(self, data):
    #     raise ValueError()

    class Meta:
        model = FinancialProfile
        exclude = ('user',)


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


