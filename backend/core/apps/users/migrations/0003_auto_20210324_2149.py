# Generated by Django 3.1.2 on 2021-03-24 21:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_waitlistuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="waitlistuser",
            name="can_register",
            field=models.BooleanField(default=False, verbose_name="Can Register"),
        ),
        migrations.AddField(
            model_name="waitlistuser",
            name="waitlist_join_dt",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Waitlist Joined Datetime",
            ),
            preserve_default=False,
        ),
    ]
