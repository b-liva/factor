# Generated by Django 2.0.2 on 2018-10-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motordb', '0003_remove_motors_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motors',
            name='ex_type',
            field=models.CharField(choices=[('safe', 'safe'), ('Exn', 'Exn'), ('ExnA', 'ExnA'), ('Exe', 'Exe'), ('Exd', 'Exd'), ('Exde', 'Exde'), (6, 'other types')], default='safe', max_length=6),
        ),
        migrations.AlterField(
            model_name='motors',
            name='ic',
            field=models.CharField(choices=[('IC411', 'IC411'), ('IC511', 'IC511'), ('IC611', 'IC611')], default='IC411', max_length=6),
        ),
        migrations.AlterField(
            model_name='motors',
            name='im',
            field=models.IntegerField(choices=[('IMB3', 'IMB3'), ('IMB35', 'IMB35')], default='IMB3'),
        ),
        migrations.AlterField(
            model_name='motors',
            name='ip',
            field=models.CharField(choices=[('IP55', 'IP55'), ('IP65', 'IP65'), ('IP23', 'IP23'), ('Other', 'Other')], default='IP55', max_length=6),
        ),
        migrations.AlterField(
            model_name='motors',
            name='kw',
            field=models.FloatField(choices=[(5.5, '5.5 kw'), (7.5, '7.5 kw'), (11, '11 kw'), (15, '15 kw'), (18.5, '18.5 kw'), (22, '22 kw'), (30, '30 kw'), (37, '37 kw'), (45, '45 kw'), (55, '55 kw'), (75, '75 kw'), (90, '90 kw'), (110, '110 kw'), (132, '132 kw'), (160, '160 kw'), (185, '185 kw'), (200, '200 kw'), (220, '220 kw'), (250, '250 kw'), (315, '315 kw'), (355, '355 kw'), (400, '400 kw'), (450, '450 kw')], default=5.5),
        ),
        migrations.AlterField(
            model_name='motors',
            name='speed',
            field=models.IntegerField(choices=[(1000, '1000 RPM'), (1500, '1500 RPM'), (3000, '3000 RPM')], default=1500),
        ),
        migrations.AlterField(
            model_name='motors',
            name='voltage',
            field=models.IntegerField(choices=[(380, '380'), (400, '400'), (3000, '3000'), (3300, '3300'), (6000, '6000'), (6600, '6600')], default=380),
        ),
    ]