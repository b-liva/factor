# Generated by Django 2.0.2 on 2019-04-14 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0004_auto_20190414_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='is_entered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payments',
            name='red_flag',
            field=models.BooleanField(default=False),
        ),
    ]