# Generated by Django 2.0.2 on 2019-04-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motordb', '0010_auto_20190417_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='motorscode',
            name='ie',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]