# Generated by Django 2.0.2 on 2019-06-15 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20190602_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='code_temp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]