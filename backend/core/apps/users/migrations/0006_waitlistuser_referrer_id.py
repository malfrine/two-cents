# Generated by Django 3.1.2 on 2021-04-23 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_waitlistuser_referral_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="waitlistuser",
            name="referrer_id",
            field=models.IntegerField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Primary Key of Referrer",
            ),
        ),
    ]
