# Generated by Django 2.0.2 on 2019-05-21 08:41

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0043_xpref_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xpref',
            name='date_modified',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
    ]
