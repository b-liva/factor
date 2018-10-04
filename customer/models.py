from django.db import models
from django.utils.timezone import now

# Create your models here.


class Type(models.Model):
    name = models.TextField()
    code = models.IntegerField()
    pub_date = models.DateTimeField(default=now)


class Customer(models.Model):
    code = models.IntegerField()
    name = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=now)
    representator = models.IntegerField(default=0)

