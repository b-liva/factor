# Generated by Django 2.0.2 on 2018-10-10 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0004_auto_20181010_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='f_id',
        ),
    ]
