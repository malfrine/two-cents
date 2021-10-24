from django.db import migrations
from django.utils import timezone

from core.apps.payments.models import PlanType


def make_default_plan_payment(apps, schema_editor):
    CurrentPaymentPlan = apps.get_model("payments", "CurrentPaymentPlan")
    User = apps.get_model("users", "User")
    for user in User.objects.all():
        try:
            CurrentPaymentPlan.objects.get(user=user)
        except CurrentPaymentPlan.DoesNotExist:
            plan_payment = CurrentPaymentPlan.objects.create(
                user=user, plan_type=PlanType.LIMITED_FREE, payment_dt=timezone.now()
            )
            plan_payment.save()


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0003_auto_20211019_0133"),
    ]

    operations = [migrations.RunPython(make_default_plan_payment)]
