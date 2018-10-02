# Generated by Django 2.0.2 on 2018-09-30 16:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0011_auto_20180930_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrefSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='', verbose_name='requests/prefactors/original/')),
                ('qty', models.IntegerField(default=1)),
                ('type', models.TextField(default=1)),
                ('price', models.FloatField(blank=True, null=True)),
                ('kw', models.FloatField()),
                ('rpm', models.IntegerField()),
                ('voltage', models.IntegerField(default=380)),
                ('ip', models.IntegerField(blank=True, null=True)),
                ('ic', models.IntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=500, null=True)),
                ('req_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Requests')),
            ],
        ),
        migrations.AlterField(
            model_name='reqspec',
            name='type',
            field=models.TextField(default=1),
        ),
    ]
