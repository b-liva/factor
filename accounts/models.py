from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
