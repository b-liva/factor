# Generated by Django 2.0.2 on 2019-10-23 13:05

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0029_auto_20191014_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='perm',
            name='date_complete',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]