# Generated by Django 2.0.2 on 2019-08-24 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('motordb', '0003_auto_20190824_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='motorscode',
            name='owner',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]