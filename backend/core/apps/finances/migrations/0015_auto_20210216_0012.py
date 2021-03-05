# Generated by Django 3.1.2 on 2021-02-16 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0014_auto_20210215_2051"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="minimum_monthly_payment",
            field=models.FloatField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Minimum Monthly Payment",
            ),
        ),
    ]