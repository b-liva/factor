# Generated by Django 2.0.2 on 2018-12-01 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_auto_20181123_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('fax', models.IntegerField(blank=True, null=True)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
                ('address', models.TextField(blank=True, max_length=600, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('add', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Address')),
            ],
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='address',
            new_name='addr',
        ),
        migrations.AddField(
            model_name='customer',
            name='postal_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer'),
        ),
    ]
