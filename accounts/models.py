from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
# from customer.models import Customer
# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    sales_exp = models.BooleanField(default=False)


class CustomerUser(User):
    is_active_customer = models.BooleanField(default=True)
    is_repr = models.BooleanField(default=True)
    # customer = models.OneToOneField(Customer, on_delete=models.DO_NOTHING)

