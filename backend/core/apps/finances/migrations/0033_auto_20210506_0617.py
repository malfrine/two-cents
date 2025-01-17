# Generated by Django 3.1.2 on 2021-05-06 06:17

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0032_auto_20210331_0606"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financialprofile",
            name="birth_date",
            field=models.DateField(
                default=datetime.datetime(1989, 3, 24, 0, 0), verbose_name="Birth Date"
            ),
        ),
        migrations.AlterField(
            model_name="financialprofile",
            name="retirement_age",
            field=models.IntegerField(default=65, verbose_name="Retirement Age"),
        ),
    ]
