# Generated by Django 2.0.2 on 2018-10-17 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0009_fund_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'permissions': (('view_expense', 'Can view expenses'),)},
        ),
        migrations.AlterModelOptions(
            name='fund',
            options={'permissions': (('view_fund', 'Can view funds'),)},
        ),
    ]