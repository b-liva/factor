# Generated by Django 2.0.2 on 2019-08-02 09:54

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0068_auto_20190802_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='due_date',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
    ]
