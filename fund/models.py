from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# Create your models here.
from factor import settings


class Fund(models.Model):
    title = models.TextField(null=True, blank=True)
    # number = models.AutoField()
    pub_date = models.DateTimeField(default=now)
    summary = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        permissions = (
            ("view_fund", "Can view funds"),
        )


class Expense(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    amount = models.FloatField()
    summary = models.TextField(null=True, blank=True)

    class Meta:
        permissions = (
            ("view_expense", "Can view expenses"),
        )
