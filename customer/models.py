from django.db import models
from django.utils.timezone import now
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User

from django import forms


# Create your models here.


def default_customer_code():
    last_customer = Customer.objects.all().order_by('pk').last()
    last_id = last_customer.pk
    customer = Customer.objects.filter(pk=last_id)
    while customer is not None:
        last_id += 1
        customer = Customer.objects.filter(code=last_id)
        if not customer:
            break
    return last_id


class Type(models.Model):
    name = models.TextField()
    code = models.IntegerField()
    pub_date = models.DateTimeField(default=now)


# types = Type.objects.all()


class Customer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    code = models.IntegerField(unique=True, default=default_customer_code, blank=True)
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    # type = models.(choices=types)
    pub_date = models.DateTimeField(default=now)
    # date2 = jmodels.jDateTimeField(default=now)
    date2 = jmodels.jDateField(default=now)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    addr = models.TextField(max_length=600, blank=True, null=True)
    agent = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('read_customer', 'Can read a customer details'),
            ('index_customer', 'Can see list of customers'),
        )

    def __str__(self):
        return '%s' % self.name


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    fax = models.IntegerField(blank=True, null=True)
    postal_code = models.IntegerField(blank=True, null=True)
    address = models.TextField(max_length=600, blank=True, null=True)


class Phone(models.Model):
    add = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
