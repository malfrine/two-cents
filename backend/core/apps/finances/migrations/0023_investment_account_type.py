# Generated by Django 3.1.2 on 2021-03-25 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0022_remove_financialprofile_monthly_allowance"),
    ]

    operations = [
        migrations.AddField(
            model_name="investment",
            name="account_type",
            field=models.CharField(
                choices=[
                    ("Non-Registered", "Non-Registered"),
                    ("RRSP", "Registered Retirement Savings Plan"),
                    ("TFSA", "Tax-Free Savings Account"),
                ],
                default="Non-Registered",
                max_length=50,
                verbose_name="Investment Account Type",
            ),
        ),
    ]
