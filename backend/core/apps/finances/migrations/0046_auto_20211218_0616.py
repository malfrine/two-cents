# Generated by Django 3.1.2 on 2021-12-18 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("finances", "0045_auto_20211216_0603"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financialdata",
            name="user",
            field=models.OneToOneField(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="financial_data",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
