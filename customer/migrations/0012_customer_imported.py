# Generated by Django 2.0.2 on 2019-06-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_customer_code_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='imported',
            field=models.BooleanField(default=False),
        ),
    ]