# Generated by Django 2.0.2 on 2019-10-14 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0026_auto_20191014_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryoutspec',
            name='serial_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]