# Generated by Django 3.1.2 on 2021-02-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0016_auto_20210216_0618"),
    ]

    operations = [
        migrations.RemoveField(model_name="investment", name="expected_volatility",),
        migrations.AddField(
            model_name="investment",
            name="prime_modifier",
            field=models.FloatField(
                blank=True, default=None, null=True, verbose_name="Prime Modifier"
            ),
        ),
        migrations.AddField(
            model_name="investment",
            name="principal_amount_invested",
            field=models.FloatField(
                blank=True, default=None, null=True, verbose_name="Amount Invested"
            ),
        ),
        migrations.AddField(
            model_name="investment",
            name="volatility_choice",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Very Low", "Very Low Volatility"),
                    ("Low", "Low Volatility"),
                    ("Medium", "Medium Volatility"),
                    ("High", "High Volatility"),
                    ("Very High", "Very High Volatility"),
                ],
                default=None,
                max_length=50,
                null=True,
                verbose_name="Volatility Choice",
            ),
        ),
        migrations.AlterField(
            model_name="investment",
            name="interest_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Mutual Fund", "Mutual Fund"),
                    ("ETF", "Exchange Traded Fund"),
                    ("GIC", "Guaranteed Investment Certificate"),
                    ("Term Deposit", "Term Deposit"),
                    ("Stock", "Stock"),
                    ("Bond", "Bond"),
                    ("Cash", "Cash"),
                ],
                default=None,
                max_length=50,
                null=True,
                verbose_name="Interest Type",
            ),
        ),
        migrations.AlterField(
            model_name="investment",
            name="investment_date",
            field=models.DateField(
                blank=True, default=None, null=True, verbose_name="Investment Date"
            ),
        ),
        migrations.AlterField(
            model_name="investment",
            name="investment_type",
            field=models.CharField(
                choices=[
                    ("Mutual Fund", "Mutual Fund"),
                    ("ETF", "Exchange Traded Fund"),
                    ("GIC", "Guaranteed Investment Certificate"),
                    ("Term Deposit", "Term Deposit"),
                    ("Stock", "Stock"),
                    ("Bond", "Bond"),
                    ("Cash", "Cash"),
                ],
                default="Mutual Fund",
                max_length=50,
                verbose_name="Investment Type",
            ),
        ),
    ]
