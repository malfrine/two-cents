# Generated by Django 3.1.2 on 2021-03-30 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0030_loan_interest_field2"),
    ]

    operations = [
        migrations.RemoveField(model_name="loan", name="apr",),
        migrations.RemoveField(model_name="loan", name="interest_type",),
        migrations.RemoveField(model_name="loan", name="prime_modifier",),
    ]
