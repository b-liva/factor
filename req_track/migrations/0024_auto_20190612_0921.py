# Generated by Django 2.0.2 on 2019-06-12 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0023_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='addr',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='tel',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
