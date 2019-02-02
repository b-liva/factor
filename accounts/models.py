from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
# from customer.models import Customer
# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    sales_exp = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.last_name

    def get_absolute_url(self):
        return reverse('account-details', args=[self.pk])


class CustomerUser(User):
    is_active_customer = models.BooleanField(default=True)
    is_repr = models.BooleanField(default=True)
    # customer = models.OneToOneField(Customer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s' % self.last_name



