# Generated by Django 2.0.2 on 2018-10-26 18:21

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='date2',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
    ]
