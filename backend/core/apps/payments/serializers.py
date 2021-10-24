from rest_framework import serializers

from core.apps.payments.models import CurrentPaymentPlan, PaymentPlanIntent


class PaymentPlanSerializer(serializers.ModelSerializer):

    expiration_dt = serializers.SerializerMethodField(source="get_expiration_dt")
    is_premium_plan = serializers.SerializerMethodField(source="get_is_premium_plan")
    is_subscription_plan = serializers.SerializerMethodField(
        source="get_is_subscription_plan"
    )
    verbose_plan_type = serializers.SerializerMethodField(
        source="get_verbose_plan_type"
    )

    def get_expiration_dt(self, obj: CurrentPaymentPlan):
        return obj.expiration_dt

    def get_is_premium_plan(self, obj: CurrentPaymentPlan):
        return obj.is_premium_plan

    def get_is_subscription_plan(self, obj: CurrentPaymentPlan):
        return obj.is_subscription_plan

    def get_verbose_plan_type(self, obj: CurrentPaymentPlan):
        return obj.get_plan_type_display()

    class Meta:
        model = CurrentPaymentPlan
        fields = (
            "id",
            "plan_type",
            "payment_dt",
            "subscription_id",
            "expiration_dt",
            "is_premium_plan",
            "is_subscription_plan",
            "is_cancelled",
            "verbose_plan_type",
        )


class PaymentPlanIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlanIntent
        exclude = ("user",)
