# Generated by Django 2.0.2 on 2019-08-24 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motordb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='motorscode',
            options={'permissions': (('list_motorscode', 'can view motor codes'),)},
        ),
    ]