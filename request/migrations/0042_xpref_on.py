# Generated by Django 2.0.2 on 2019-05-21 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0041_xpref_to_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='xpref',
            name='on',
            field=models.BooleanField(default=False),
        ),
    ]