# Generated by Django 2.0.2 on 2019-08-17 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reqspec',
            options={'permissions': (('index_reqspecs', 'can see list of request Specs'), ('index_reqspec', 'can see list of request Spec!'), ('read_reqspecs', 'can read request Specs'))},
        ),
    ]
