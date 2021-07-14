# Generated by Django 3.1.2 on 2021-07-11 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0035_auto_20210514_0639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='mortgage_details',
        ),
        migrations.AddField(
            model_name='loan',
            name='current_term_end_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Current Term End Date'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='investment_type',
            field=models.CharField(choices=[('Mutual Fund', 'Mutual Fund'), ('ETF', 'Exchange Traded Fund'), ('GIC', 'Guaranteed Investment Certificate'), ('Term Deposit', 'Term Deposit'), ('Stock', 'Stock'), ('Bond', 'Bond'), ('Cash', 'Cash'), ('Portfolio', 'Portfolio')], default='Mutual Fund', max_length=50, verbose_name='Investment Type'),
        ),
        migrations.DeleteModel(
            name='MortgageDetails',
        ),
    ]
