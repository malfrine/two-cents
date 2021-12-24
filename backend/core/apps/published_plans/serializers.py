from rest_framework import serializers

from core.apps.finances.serializers.serializers import FinancialDataSerializer
from core.apps.published_plans.models import PublishedPlan


class PublishedPlanSerializer(serializers.ModelSerializer):

    financial_data = FinancialDataSerializer()

    class Meta:
        model = PublishedPlan
        fields = ("id", "financial_data")
