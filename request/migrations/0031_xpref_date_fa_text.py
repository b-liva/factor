# Generated by Django 2.0.2 on 2019-11-12 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0030_perm_date_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='xpref',
            name='date_fa_text',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]