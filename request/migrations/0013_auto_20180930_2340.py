# Generated by Django 2.0.2 on 2018-09-30 20:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0012_auto_20180930_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Xpref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='', verbose_name='requests/views/original/')),
                ('req_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Requests')),
            ],
        ),
        migrations.RemoveField(
            model_name='prefspec',
            name='image',
        ),
        migrations.RemoveField(
            model_name='prefspec',
            name='number',
        ),
        migrations.RemoveField(
            model_name='prefspec',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='prefspec',
            name='req_id',
        ),
        migrations.AddField(
            model_name='prefspec',
            name='xpref_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='request.Xpref'),
            preserve_default=False,
        ),
    ]
