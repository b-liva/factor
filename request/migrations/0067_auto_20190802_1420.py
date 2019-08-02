# Generated by Django 2.0.2 on 2019-08-02 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0066_auto_20190724_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='PyamentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.PyamentType'),
        ),
    ]
