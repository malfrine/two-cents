from django.db import migrations

from core.apps.finances.models.constants import InterestTypes


def transfer_loan_data_to_interest(apps, schema_editor):
    LoanInterest = apps.get_model("finances", "LoanInterest")
    Loan = apps.get_model("finances", "Loan")
    for loan in Loan.objects.all():
        interest_type = loan.interest_type
        apr = None if interest_type == InterestTypes.VARIABLE else loan.apr
        prime_modifier = (
            None if interest_type == InterestTypes.FIXED else loan.prime_modifier
        )
        loan.loan_interest = LoanInterest.objects.create(
            interest_type=interest_type, apr=apr, prime_modifier=prime_modifier
        )
        loan.save()


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0029_loan_interest_field"),
    ]

    operations = [migrations.RunPython(transfer_loan_data_to_interest)]
