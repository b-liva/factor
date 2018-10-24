# Generated by Django 2.0.2 on 2018-10-12 06:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MotorDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kw', models.FloatField()),
                ('speed', models.IntegerField()),
                ('voltage', models.IntegerField()),
                ('prime_cost', models.FloatField()),
                ('base_price', models.FloatField()),
                ('sale_price', models.FloatField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='PriceDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('summary', models.TextField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='PrimeCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kw5_5', models.FloatField()),
                ('price_db', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricedb.PriceDb')),
            ],
        ),
    ]