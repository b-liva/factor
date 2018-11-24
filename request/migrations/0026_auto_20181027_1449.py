# Generated by Django 2.0.2 on 2018-10-27 10:49

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0025_reqspec_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='xpref',
            name='date_fa',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='xpref',
            name='exp_date_fa',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
    ]