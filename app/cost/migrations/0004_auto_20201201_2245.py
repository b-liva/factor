# Generated by Django 2.0.2 on 2020-12-01 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cost', '0003_projectcost_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectcost',
            options={'permissions': [('read_projectcost', 'can read projectcost')]},
        ),
    ]
