# Generated by Django 2.0.2 on 2018-10-24 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motordb', '0016_auto_20181024_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motors',
            name='kw',
            field=models.IntegerField(blank=True, choices=[(0, '5.5 kw'), (1, '7.5 kw'), (2, '11 kw'), (3, '15 kw'), (4, '18.5 kw'), (5, '22 kw'), (6, '30 kw'), (7, '37 kw'), (8, '45 kw'), (9, '55 kw'), (10, '75 kw'), (11, '90 kw'), (12, '110 kw'), (13, '132 kw'), (14, '160 kw'), (15, '185 kw'), (16, '200 kw'), (17, '220 kw'), (18, '250 kw'), (19, '280 kw'), (20, '315 kw'), (21, '355 kw'), (22, '400 kw'), (23, '450 kw'), (24, '500 kw'), (25, '560 kw'), (26, '630 kw'), (27, '710 kw'), (28, '800 kw'), (29, '900 kw'), (30, '1000 kw'), (31, '1120 kw'), (32, '1250 kw'), (33, '1400 kw'), (34, '1600 kw'), (35, '1800 kw'), (36, '2000 kw')], default=7, null=True),
        ),
    ]
