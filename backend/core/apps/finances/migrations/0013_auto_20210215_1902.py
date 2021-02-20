# Generated by Django 3.1.2 on 2021-02-15 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0012_financialprofile_risk_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="financialprofile",
            name="risk_profile",
        ),
        migrations.AddField(
            model_name="financialprofile",
            name="risk_tolerance",
            field=models.FloatField(default=0.5, verbose_name="Risk Tolerance"),
        ),
    ]
