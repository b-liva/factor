# Generated by Django 2.0.2 on 2019-08-25 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricedb', '0004_remove_motordb_pub_date2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='motordb',
            old_name='motor',
            new_name='code',
        ),
    ]
