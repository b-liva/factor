# Generated by Django 2.0.2 on 2018-12-06 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0046_reqspec_sent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'permissions': (('read_payment', 'Can read payment details'), ('index_payment', 'Can see list of payments'))},
        ),
    ]
