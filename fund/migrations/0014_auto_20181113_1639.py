# Generated by Django 2.0.2 on 2018-11-13 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0013_auto_20181113_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund',
            name='summary',
            field=models.TextField(blank=True, max_length=600, null=True),
        ),
    ]
