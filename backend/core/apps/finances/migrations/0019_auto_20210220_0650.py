# Generated by Django 3.1.2 on 2021-02-20 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0018_auto_20210219_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='current_balance',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Current Balance'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='interest_type',
            field=models.CharField(blank=True, choices=[('Fixed', 'Fixed Interest Rate'), ('Variable', 'Variable Interest Rate')], default=None, max_length=50, null=True, verbose_name='Interest Type'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='pre_authorized_monthly_contribution',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Pre-Authorized Monthly Contribution'),
        ),
    ]
