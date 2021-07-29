# Generated by Django 3.1.2 on 2021-03-25 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0024_mortgage"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mortgage",
            old_name="amortization_period_years",
            new_name="amortization_years",
        ),
        migrations.AlterField(
            model_name="mortgage",
            name="current_term_interest_type",
            field=models.CharField(
                choices=[
                    ("Fixed", "Fixed Interest Rate"),
                    ("Variable", "Variable Interest Rate"),
                ],
                default="Fixed",
                max_length=50,
                verbose_name="Current Term Interest Type",
            ),
        ),
    ]
