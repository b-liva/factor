# Generated by Django 2.0.2 on 2019-04-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0017_auto_20190415_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackxpref',
            name='req_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
