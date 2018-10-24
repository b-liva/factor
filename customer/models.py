from django.db import models
from django.utils.timezone import now
from django import forms

# Create your models here.


class Type(models.Model):
    name = models.TextField()
    code = models.IntegerField()
    pub_date = models.DateTimeField(default=now)


# types = Type.objects.all()


class Customer(models.Model):
    code = models.IntegerField()
    name = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    # type = models.(choices=types)
    pub_date = models.DateTimeField(default=now)
    representator = models.IntegerField(default=0)

