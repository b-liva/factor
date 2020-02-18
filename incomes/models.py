import os.path
from os.path import split

# from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, F, FloatField
from django.utils import timezone


from django.db import models
import datetime
import jdatetime
from django.utils.timezone import now
from django_jalali.db import models as jmodels

from django.contrib.auth import get_user_model

from customer.models import Customer

User = get_user_model()

# Create your models here.
from request.models import Xpref, PaymentType, TimeStampedModel, Perm


class Income(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    number = models.IntegerField(unique=True)
    type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, blank=True, null=True)
    amount = models.FloatField()
    date_fa = jmodels.jDateField(default=now)
    due_date = jmodels.jDateField(blank=True, null=True)
    summary = models.TextField(max_length=600, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def pub_date_pretty(self):
        return self.date_fa.strftime('%b %e %Y')

    def __str__(self):
        return '#%s - amount:%s - customer:%s' % (self.number, self.amount, self.customer)

    def assigned(self):
        from django.db.models import Sum
        assigned = self.incomerow_set.aggregate(sum=Sum('amount'))
        if assigned['sum'] is not None:
            return assigned['sum']
        return 0

    def not_assigned(self):
        not_assigned = self.amount - self.assigned()
        return not_assigned

    class Meta:
        permissions = (
            ('read_payment', 'Can read payment details'),
            ('index_payment', 'Can see list of payments'),
        )


class IncomeRow(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    income = models.ForeignKey(Income, on_delete=models.CASCADE)
    proforma = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    perm = models.ForeignKey(Perm, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.FloatField()
    date_fa = jmodels.jDateField(default=now)
    summary = models.TextField(max_length=600, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "مبلغ %s از %s" % (self.amount, self.income)
