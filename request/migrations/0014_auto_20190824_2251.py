# Generated by Django 2.0.2 on 2019-08-24 18:21

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0013_auto_20190824_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proformafollowup',
            name='next_followup',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]
