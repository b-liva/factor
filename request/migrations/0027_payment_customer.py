# Generated by Django 2.0.2 on 2018-10-27 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20181027_1235'),
        ('request', '0026_auto_20181027_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='customer.Customer'),
            preserve_default=False,
        ),
    ]
