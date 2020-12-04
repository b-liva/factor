# Generated by Django 2.0.2 on 2020-08-22 04:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ManyToManyField(related_name='user_child', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ManyToManyField(related_name='user_parent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]