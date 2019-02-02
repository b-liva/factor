from django.db import models
from django.db.models import Q

from django.utils.timezone import now

# Create your models here.

# class MotorDb(models.Model):
#     kw = models.FloatField()
#     speed = models.IntegerField()
#     voltage = models.IntegerField()
#     pub_date = models.DateTimeField(default=now)

kw = (
    (0, '5.5 kw'),
    (1, '7.5 kw'),
    (2, '11 kw'),
    (3, '15 kw'),
    (4, '18.5 kw'),
    (5, '22 kw'),
    (6, '30 kw'),
    (7, '37 kw'),
    (8, '45 kw'),
    (9, '55 kw'),
    (10, '75 kw'),
    (11, '90 kw'),
    (12, '110 kw'),
    (13, '132 kw'),
    (14, '160 kw'),
    (15, '185 kw'),
    (16, '200 kw'),
    (17, '220 kw'),
    (18, '250 kw'),
    (19, '280 kw'),
    (20, '315 kw'),
    (21, '355 kw'),
    (22, '400 kw'),
    (23, '450 kw'),
    (24, '500 kw'),
    (25, '560 kw'),
    (26, '630 kw'),
    (27, '710 kw'),
    (28, '800 kw'),
    (29, '900 kw'),
    (30, '1000 kw'),
    (31, '1120 kw'),
    (32, '1250 kw'),
    (33, '1400 kw'),
    (34, '1600 kw'),
    (35, '1800 kw'),
    (36, '2000 kw'),
)

voltage = (
    (0, '380'),
    (1, '400'),
    (2, '3000'),
    (3, '3300'),
    (4, '6000'),
    (5, '6600'),
)

ex_types = (
    (0, 'safe'),
    (1, 'Exn'),
    (2, 'ExnA'),
    (3, 'Exe'),
    (4, 'Exd'),
    (5, 'Exde'),
    (6, 'other types'),
)

speed = (
    (3, '750 RPM'),
    (0, '1000 RPM'),
    (1, '1500 RPM'),
    (2, '3000 RPM'),
)

im = (
    (0, 'IMB3'),
    (1, 'IMB35'),
)

ic = (
    (0, 'IC411'),
    (1, 'IC511'),
    (2, 'IC611'),
)

ip = (
    (0, 'IP55'),
    (1, 'IP65'),
    (2, 'IP23'),
    (3, 'Other'),
)


class Motors(models.Model):
    type = models.CharField(max_length=20)
    kw = models.IntegerField(choices=kw, default=7, null=True, blank=True)
    frame_size = models.CharField(max_length=6)
    speed = models.IntegerField(choices=speed, default=1, null=True, blank=True)
    voltage = models.IntegerField(choices=voltage, default=0, null=True, blank=True)
    ip = models.IntegerField(choices=ip, default=0, null=True, blank=True)
    ic = models.IntegerField(choices=ic, default=0, null=True, blank=True)
    ex_type = models.IntegerField(choices=ex_types, default=0)
    # images = models.FileField(upload_to='motordb/')

    efficiency = models.FloatField()
    PF = models.FloatField()
    current_ln = models.FloatField()
    current_ls_to_ln = models.FloatField()
    torque_tn = models.FloatField()
    torque_ts_to_tn = models.FloatField()
    torque_tmax_to_tn = models.FloatField()
    torque_rotor_inertia = models.FloatField()
    weight = models.FloatField()

    freq = models.FloatField(default=50)
    im = models.IntegerField(choices=im, default=0)

    summary = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        permissions = (
            ('view_motordb', 'can view motor database'),
            ('index_motordb', 'can view list of motor database'),
        )


class MotorsCode(models.Model):
    code = models.CharField(max_length=15, unique=True)
    kw = models.DecimalField(max_digits=7, decimal_places=1)
    frame_size = models.CharField(max_length=6, blank=True, null=True)
    speed = models.IntegerField()
    voltage = models.IntegerField(null=True, blank=True)
    ip = models.IntegerField(null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    im = models.CharField(max_length=8, null=True, blank=True)
    yd = models.CharField(max_length=10, null=True, blank=True)
    # ex_type = models.IntegerField(choices=ex_types, default=0, null=True, blank=True)
    # images = models.FileField(upload_to='motordb/')
    efficiency = models.FloatField(null=True, blank=True)
    pf = models.FloatField(null=True, blank=True)
    current_ln = models.FloatField(null=True, blank=True)
    current_ls_to_ln = models.FloatField(null=True, blank=True)
    torque_tn = models.FloatField(null=True, blank=True)
    torque_ts_to_tn = models.FloatField(null=True, blank=True)
    torque_tmax_to_tn = models.FloatField(null=True, blank=True)
    torque_rotor_inertia = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    freq = models.FloatField(default=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    summary = models.TextField(max_length=700, blank=True, null=True)

    def __str__(self):
        return '%s kw - %s rpm - %s V' % (self.kw, self.speed, self.voltage)


class MotorsPrice(models.Model):
    code = models.CharField(max_length=15, unique=True)
    kw = models.DecimalField(max_digits=7, decimal_places=1)
    frame_size = models.CharField(max_length=6, blank=True, null=True)
    speed = models.IntegerField()
    voltage = models.IntegerField(null=True, blank=True)
    ip = models.IntegerField(null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    im = models.CharField(max_length=8, null=True, blank=True)
    yd = models.CharField(max_length=10, null=True, blank=True)
    # ex_type = models.IntegerField(choices=ex_types, default=0, null=True, blank=True)
    # images = models.FileField(upload_to='motordb/')
    efficiency = models.FloatField(null=True, blank=True)
    pf = models.FloatField(null=True, blank=True)
    current_ln = models.FloatField(null=True, blank=True)
    current_ls_to_ln = models.FloatField(null=True, blank=True)
    torque_tn = models.FloatField(null=True, blank=True)
    torque_ts_to_tn = models.FloatField(null=True, blank=True)
    torque_tmax_to_tn = models.FloatField(null=True, blank=True)
    torque_rotor_inertia = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    freq = models.FloatField(default=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    summary = models.TextField(max_length=700, blank=True, null=True)

    def __str__(self):
        return '%s kw - %s rpm - %s V' % (self.kw, self.speed, self.voltage)
