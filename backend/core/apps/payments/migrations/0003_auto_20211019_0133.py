# Generated by Django 3.1.2 on 2021-10-19 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_auto_20211017_2140"),
    ]

    operations = [
        migrations.RenameField(
            model_name="paymentplanintent",
            old_name="payment_intent_id",
            new_name="stripe_id",
        ),
        migrations.RemoveField(model_name="paymentplanintent", name="subscription_id",),
    ]
