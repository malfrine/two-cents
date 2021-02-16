# Generated by Django 3.1.2 on 2021-02-02 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0007_auto_20210202_0436"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="interest_type",
            field=models.CharField(
                choices=[
                    ("Fixed Interest Rate", "Fixed Interest Rate"),
                    ("Variable Interest Rate", "Variable Interest Rate"),
                ],
                default="Fixed Interest Rate",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="loan_type",
            field=models.CharField(
                choices=[
                    ("Credit Card", "Credit Card"),
                    ("Line of Credit", "Line Of Credit"),
                    ("Student Loan", "Student Loan"),
                    ("Student Line of Credit", "Student Line of Credit"),
                    ("Personal Loan", "Personal Loan"),
                ],
                default="Personal Loan",
                max_length=50,
            ),
        ),
    ]
