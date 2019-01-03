# from django.contrib.auth.models import User
from accounts.models import User
from django.db import models
from django.utils.timezone import now
from django_jalali.db import models as jmodels


# Create your models here.
from factor import settings


class Fund(models.Model):
    objects = jmodels.jManager()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150, null=True, blank=True)
    pub_date = models.DateTimeField(default=now)
    date_fa = jmodels.jDateField(default=now)
    summary = models.TextField(max_length=600, null=True, blank=True)

    class Meta:
        permissions = (
            ("view_fund", "Can view funds"),
            ("index_fund", "Can view list of funds"),
        )

    def __str__(self):
        return '%s' % self.title


class Expense(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    amount = models.IntegerField()
    summary = models.TextField(max_length=600, null=True, blank=True)

    class Meta:
        permissions = (
            ("view_expense", "Can view expenses"),
        )

    def __str__(self):
        return 'expense:%s - $%s' % (self.title, self.amount)


