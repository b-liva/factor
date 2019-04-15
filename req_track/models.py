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


class Track_xpref(models.Model):
    req_number = models.CharField(max_length=40)

    number = models.IntegerField(unique=True)
    date_fa = models.CharField(max_length=15)
    exp_date_fa = models.CharField(max_length=15, null=True, blank=True)
    perm_number = models.CharField(max_length=10, null=True, blank=True)

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
