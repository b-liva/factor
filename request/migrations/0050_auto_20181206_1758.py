# Generated by Django 2.0.2 on 2018-12-06 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0049_auto_20181206_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.Customer'),
        ),
    ]
