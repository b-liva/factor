# Generated by Django 2.0.2 on 2019-04-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0028_auto_20190414_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prefspec',
            name='qty_sent',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]