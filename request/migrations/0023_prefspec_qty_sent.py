# Generated by Django 2.0.2 on 2019-04-13 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0022_auto_20190318_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='prefspec',
            name='qty_sent',
            field=models.IntegerField(default=1),
        ),
    ]