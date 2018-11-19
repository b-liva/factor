# Generated by Django 2.0.2 on 2018-11-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0043_remove_reqspec_images'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'permissions': (('read_payment', 'Can read a customer details'), ('index_payment', 'Can see list of customers'))},
        ),
        migrations.AlterModelOptions(
            name='reqspec',
            options={'permissions': (('index_reqspecs', 'can see list of request Specs'), ('read_reqspecs', 'can read request Specs'))},
        ),
        migrations.AddField(
            model_name='prefspec',
            name='considerations',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
