# Generated by Django 2.0.2 on 2019-01-17 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20190117_1207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': (('read_customer', 'Can read a customer details'), ('index_customer', 'Can see list of customers'), ('index_requests', 'customer can see list of requests'))},
        ),
    ]
