# Generated by Django 2.0.2 on 2019-11-19 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0037_auto_20191119_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('code', models.BigIntegerField(default=55005500)),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('ph', models.FloatField(default=1)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Requests')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='wastage',
            old_name='details',
            new_name='title',
        ),
        migrations.AddField(
            model_name='wastage',
            name='qty',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='reqpart',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]
