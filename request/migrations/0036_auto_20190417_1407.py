# Generated by Django 2.0.2 on 2019-04-17 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0035_auto_20190417_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='prefspec',
            name='ic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.ICType'),
        ),
        migrations.AddField(
            model_name='prefspec',
            name='im',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IMType'),
        ),
        migrations.AddField(
            model_name='prefspec',
            name='ip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IPType'),
        ),
    ]