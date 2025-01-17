# Generated by Django 3.1.2 on 2021-03-31 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0031_auto_20210330_0514"),
    ]

    operations = [
        migrations.CreateModel(
            name="MortgageDetails",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("monthly_payment", models.FloatField(verbose_name="Monthly Payment")),
                (
                    "purchase_price",
                    models.FloatField(verbose_name="House Purchase Price"),
                ),
                ("purchase_date", models.DateField(verbose_name="Purchase Date")),
                ("downpayment_amount", models.FloatField(verbose_name="Downpayment")),
                (
                    "amortization_years",
                    models.FloatField(verbose_name="Amortization Period in Years"),
                ),
                (
                    "current_term_start_date",
                    models.DateField(verbose_name="Current Term Start Date"),
                ),
                (
                    "current_term_years",
                    models.FloatField(verbose_name="Current Term Length in Years"),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="loan",
            name="current_balance",
            field=models.FloatField(
                blank=True, default=None, null=True, verbose_name="Current Balance"
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="loan_interest",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="loan_interest",
                to="finances.loaninterest",
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="loan_type",
            field=models.CharField(
                choices=[
                    ("Credit Card", "Credit Card Loan"),
                    ("Line of Credit", "Line Of Credit"),
                    ("Student Loan", "Student Loan"),
                    ("Student Line of Credit", "Student Line of Credit"),
                    ("Personal Loan", "Personal Loan"),
                    ("Car Loan", "Car Loan"),
                    ("Mortgage", "Mortgage"),
                ],
                default="Personal Loan",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="loan",
            name="mortgage_details",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mortgage_details",
                to="finances.mortgagedetails",
            ),
        ),
    ]
