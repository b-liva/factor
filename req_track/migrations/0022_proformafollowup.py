# Generated by Django 2.0.2 on 2019-05-20 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0021_auto_20190416_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProformaFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=15)),
                ('date', models.CharField(max_length=15)),
                ('number', models.CharField(max_length=15)),
                ('details', models.TextField(blank=True, null=True)),
                ('customer', models.CharField(blank=True, max_length=50, null=True)),
                ('result', models.TextField()),
            ],
        ),
    ]