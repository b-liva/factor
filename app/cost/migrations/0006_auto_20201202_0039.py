# Generated by Django 2.0.2 on 2020-12-01 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cost', '0005_auto_20201202_0031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wagecost',
            options={'permissions': [('read_wagecost', 'can retrieve wage cost')]},
        ),
    ]
