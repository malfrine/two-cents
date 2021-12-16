from django.conf import settings

from django.db import migrations


def nullify_user_attr_on_financial_objects(apps, schema_editor):
    FinancialProfile = apps.get_model("finances", "FinancialProfile")
    for financial_profile in FinancialProfile.objects.all():
        financial_profile.user = None
        financial_profile.save()
    Loan = apps.get_model("finances", "Loan")
    for loan in Loan.objects.all():
        loan.user = None
        loan.save()
    Investment = apps.get_model("finances", "Investment")
    for investment in Investment.objects.all():
        investment.user = None
        investment.save()
    Goal = apps.get_model("finances", "FinancialGoal")
    for goal in Goal.objects.all():
        goal.user = None
        goal.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("finances", "0043_auto_20211216_0052"),
    ]

    operations = [migrations.RunPython(nullify_user_attr_on_financial_objects)]
