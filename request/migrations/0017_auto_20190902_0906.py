# Generated by Django 2.0.2 on 2019-09-02 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0016_reqparts_req'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReqParts',
            new_name='ReqPart',
        ),
    ]
