# Generated by Django 2.0.2 on 2018-10-27 12:13

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0027_payment_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date_fa',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now),
        ),
    ]
