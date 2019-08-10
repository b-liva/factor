# Generated by Django 2.0.2 on 2019-08-10 10:36

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
                ('voltage', models.IntegerField(default=380)),
                ('prime_cost', models.FloatField(blank=True, null=True)),
                ('base_price', models.FloatField(blank=True, null=True)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'permissions': (('view_pricedb', 'can view price database'), ('clean_pricedb', 'can view price database')),
            },
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
        migrations.CreateModel(
            name='SalesPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('price', models.IntegerField()),
                ('price_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricedb.PriceDb')),
            ],
        ),
        migrations.AddField(
            model_name='motordb',
            name='price_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricedb.PriceDb'),
        ),
    ]
