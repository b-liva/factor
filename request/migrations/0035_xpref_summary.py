# Generated by Django 2.0.2 on 2018-11-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0034_auto_20181105_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='xpref',
            name='summary',
            field=models.TextField(blank=True, max_length=600, null=True),
        ),
    ]