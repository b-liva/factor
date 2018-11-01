from django.db import models
from django.utils.timezone import now
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User

from django import forms

# Create your models here.


class Type(models.Model):
    name = models.TextField()
    code = models.IntegerField()
    pub_date = models.DateTimeField(default=now)


# types = Type.objects.all()


class Customer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    code = models.IntegerField()
    name = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    # type = models.(choices=types)
    pub_date = models.DateTimeField(default=now)
    # date2 = jmodels.jDateTimeField(default=now)
    date2 = jmodels.jDateField(default=now)
    representator = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ('read_customer', 'Can read a customer details'),
            ('index_customer', 'Can see list of customers'),
        )

