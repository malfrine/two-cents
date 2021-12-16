from django.db import migrations


def connect_financial_data_to_financial_objects(apps, schema_editor):
    User = apps.get_model("users", "User")
    FinancialData = apps.get_model("finances", "FinancialData")
    for user in User.objects.all():
        financial_data = FinancialData.objects.create(user=user)
        financial_data.save()

    FinancialProfile = apps.get_model("finances", "FinancialProfile")
    for financial_profile in FinancialProfile.objects.all():
        financial_data = FinancialData.objects.get(user=financial_profile.user)
        financial_profile.financial_data = financial_data
        financial_profile.save()
    Loan = apps.get_model("finances", "Loan")
    for loan in Loan.objects.all():
        financial_data = FinancialData.objects.get(user=loan.user)
        loan.financial_data = financial_data
        loan.save()
    Investment = apps.get_model("finances", "Investment")
    for investment in Investment.objects.all():
        financial_data = FinancialData.objects.get(user=investment.user)
        investment.financial_data = financial_data
        investment.save()
    Goal = apps.get_model("finances", "FinancialGoal")
    for goal in Goal.objects.all():
        financial_data = FinancialData.objects.get(user=goal.user)
        goal.financial_data = financial_data
        goal.save()


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0039_auto_20211215_0642"),
    ]

    operations = [migrations.RunPython(connect_financial_data_to_financial_objects)]
