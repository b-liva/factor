# Generated by Django 2.0.2 on 2019-05-29 06:55

from django.db import migrations
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0050_comment_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_fa',
            field=django_jalali.db.models.jDateField(default=django.utils.timezone.now),
        ),
    ]