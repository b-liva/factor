# Generated by Django 2.0.2 on 2019-09-02 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0014_auto_20190824_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReqParts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
            ],
        ),
    ]