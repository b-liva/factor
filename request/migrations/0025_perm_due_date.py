# Generated by Django 2.0.2 on 2019-10-14 08:42

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0024_auto_20191013_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='perm',
            name='due_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]
