# Generated by Django 2.0.2 on 2019-04-15 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0008_auto_20190415_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackitemscode',
            name='code',
            field=models.BigIntegerField(),
        ),
    ]