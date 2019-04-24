# Generated by Django 2.0.2 on 2019-04-16 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('req_track', '0020_trackitemscode_temp_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackitemscode',
            name='current_ln',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='current_ls_to_ln',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='efficiency',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='frame_size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='freq',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='ic',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='im',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='ip',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='kw',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='pf',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='speed',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='torque_rotor_inertia',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='torque_tmax_to_tn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='torque_tn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='torque_ts_to_tn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='voltage',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='weight',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trackitemscode',
            name='yd',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]