# Generated by Django 2.0.2 on 2019-05-20 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0039_auto_20190420_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='xpref',
            name='follow_up',
            field=models.TextField(blank=True, null=True),
        ),
    ]
