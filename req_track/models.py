from django.db import models
from accounts.models import User
from django.utils.timezone import now
from django_jalali.db import models as jmodels


# Create your models here.
# class ReceivedBy(models.Model):
#     title = models.CharField(max_length=15)
#
#     def __str__(self):
#         return '%s' % self.title
from request.models import ReqSpec


class ReqEntered(models.Model):
    number_entered = models.CharField(max_length=20, blank=True, null=True)
    number_automation = models.IntegerField(unique=True)
    # received_by = models.ForeignKey(ReceivedBy, on_delete=models.DO_NOTHING)
    is_entered = models.BooleanField(default=False)
    title = models.CharField(max_length=250, null=True, blank=True)
    # owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    owner_text = models.CharField(max_length=40, default='الوند')
    date_txt = models.CharField(max_length=12, null=True, blank=True)
    customer = models.CharField(max_length=200, null=True, blank=True)
    is_request = models.BooleanField(default=True)
    attachment = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=600, null=True, blank=True)
    # date_fa = jmodels.jDateField(default=now, null=True, blank=True)

    def __str__(self):
        return '%s' % self.number_automation


class TrackXpref(models.Model):
    code = models.CharField(max_length=40)
    number = models.IntegerField(unique=True)
    req_number = models.CharField(max_length=40)
    qty = models.IntegerField()
    price = models.FloatField()
    date_fa = models.CharField(max_length=15)
    exp_date_fa = models.CharField(max_length=15, null=True, blank=True)
    perm_number = models.CharField(max_length=10, null=True, blank=True)
    red_flag = models.BooleanField(default=False)
    is_entered = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.number


class Payments(models.Model):
    number = models.CharField(max_length=20)
    prof_number = models.CharField(max_length=40)
    date_txt = models.CharField(max_length=12, null=True, blank=True)
    date = jmodels.jDateField(blank=True, null=True)
    amount = models.FloatField()
    type = models.CharField(max_length=10)
    is_entered = models.BooleanField(default=False)
    red_flag = models.BooleanField(default=False)

    def __str__(self):
        return '#%s - $%s' % (self.number, self.amount)


class TrackItemsCode(models.Model):
    code = models.BigIntegerField()
    kw = models.DecimalField(max_digits=7, decimal_places=1, null=True, blank=True)
    frame_size = models.CharField(max_length=6, blank=True, null=True)
    speed = models.IntegerField(null=True, blank=True)
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
    details = models.TextField()
