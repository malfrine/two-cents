# Generated by Django 3.1.2 on 2021-03-30 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0026_auto_20210326_0452"),
    ]

    operations = [
        migrations.DeleteModel(name="Mortgage",),
    ]
