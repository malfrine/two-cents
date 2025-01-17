# Generated by Django 3.1.2 on 2021-02-02 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0006_auto_20210130_0040"),
    ]

    operations = [
        migrations.AddField(
            model_name="loan",
            name="prime_modifier",
            field=models.FloatField(null=True, verbose_name="Prime Modifier"),
        ),
        migrations.AlterField(
            model_name="loan",
            name="apr",
            field=models.FloatField(null=True, verbose_name="APR"),
        ),
    ]
