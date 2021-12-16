from django.db import migrations


def connect_financial_data_to_financial_goals(apps, schema_editor):
    FinancialData = apps.get_model("finances", "FinancialData")
    Goal = apps.get_model("finances", "FinancialGoal")
    for goal in Goal.objects.all():
        financial_data = FinancialData.objects.get(user=goal.user)
        goal.financial_data = financial_data
        goal.save()


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0040_separate_users_and_finances"),
    ]

    operations = [migrations.RunPython(connect_financial_data_to_financial_goals)]
