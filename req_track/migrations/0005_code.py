# Generated by Django 2.0.2 on 2019-12-30 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0004_tadvintotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.BigIntegerField()),
                ('kw', models.CharField(blank=True, max_length=50, null=True)),
                ('frame', models.CharField(blank=True, max_length=50, null=True)),
                ('speed', models.CharField(blank=True, max_length=50, null=True)),
                ('voltage', models.CharField(blank=True, max_length=50, null=True)),
                ('ip', models.CharField(blank=True, max_length=50, null=True)),
                ('ic', models.CharField(blank=True, max_length=50, null=True)),
                ('im', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('weight', models.CharField(blank=True, max_length=50, null=True)),
                ('details', models.TextField()),
                ('red_flag', models.BooleanField(default=False)),
                ('green_flag', models.BooleanField(default=False)),
                ('is_entered', models.BooleanField(default=False)),
                ('temp_str', models.TextField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
