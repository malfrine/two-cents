# Generated by Django 3.1.2 on 2020-12-16 02:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("finances", "0004_auto_20201208_0212"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financialprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="financial_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="investment",
            name="risk_level",
            field=models.CharField(
                choices=[
                    ("Low", "Low Risk"),
                    ("Medium", "Medium Risk"),
                    ("High", "High Risk"),
                ],
                default="Medium",
                max_length=50,
                verbose_name="Risk Type",
            ),
        ),
    ]
