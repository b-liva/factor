# Generated by Django 2.0.2 on 2019-08-24 18:20

import datetime
from django.db import migrations
from django.utils.timezone import utc
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0012_auto_20190824_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proformafollowup',
            name='next_followup',
            field=django_jalali.db.models.jDateField(default=datetime.datetime(2019, 8, 24, 18, 20, 39, 709858, tzinfo=utc)),
        ),
    ]
