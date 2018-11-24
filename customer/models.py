from django.db import models
from django.utils.timezone import now
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User

from django import forms

# Create your models here.


def default_customer_code():
    last_customer = Customer.objects.all().order_by('pk').last()
    last_id = last_customer.pk
    print(last_id)
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
    representator = models.IntegerField(default=0)
    phone = models.IntegerField(blank=True, null=True)
    fax = models.IntegerField(blank=True, null=True)
    address = models.TextField(max_length=600, blank=True, null=True)

    class Meta:
        permissions = (
            ('read_customer', 'Can read a customer details'),
            ('index_customer', 'Can see list of customers'),
        )

    def __str__(self):
        return '%s' % self.name

