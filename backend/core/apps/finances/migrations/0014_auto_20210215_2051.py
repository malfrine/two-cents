# Generated by Django 3.1.2 on 2021-02-15 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0013_auto_20210215_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialprofile',
            name='risk_tolerance',
            field=models.FloatField(default=50.0, verbose_name='Risk Tolerance'),
        ),
    ]
