# Generated by Django 2.0.2 on 2019-09-14 07:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_list_id', models.IntegerField()),
                ('price_list_name', models.CharField(max_length=40)),
                ('kw', models.FloatField()),
                ('rpm', models.IntegerField()),
                ('code', models.BigIntegerField()),
                ('prime_cost', models.FloatField(blank=True, null=True)),
                ('base_price', models.FloatField()),
                ('sale_price', models.FloatField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]