# Generated by Django 2.0.2 on 2019-01-06 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_user',
        ),
    ]
