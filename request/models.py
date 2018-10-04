from django.db import models
import datetime
from django.utils.timezone import now
from customer.models import Customer

class Requests(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.FileField('requests/', null=True, blank=True)

    summary = models.TextField(max_length=1000, null=True, blank=True)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class ReqSpec(models.Model):
    req_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    type = models.TextField(default=1)
    # probably this price should be removed.
    price = models.FloatField(null=True, blank=True)
    kw = models.FloatField()
    rpm = models.IntegerField()
    voltage = models.IntegerField(default=380)
    ip = models.IntegerField(null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    summary = models.TextField(max_length=500, blank=True, null=True)


class Xpref(models.Model):
    req_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField('requests/prefactors/original/')

class PrefSpec(models.Model):
    xpref_id = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    type = models.TextField(default=1)
    price = models.FloatField(null=True, blank=True)
    kw = models.FloatField()
    rpm = models.IntegerField()
    voltage = models.IntegerField(default=380)
    ip = models.IntegerField(null=True, blank=True)
    ic = models.IntegerField(null=True, blank=True)
    summary = models.TextField(max_length=500, blank=True, null=True)


class XprefVerf(models.Model):
    xpref = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField('requests/prefactors/verifications/')
    summary = models.TextField(max_length=1000)

class Prefactor(models.Model):
    request_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField('requests/prefactors/original/')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class PrefactorVerification(models.Model):
    pref_id = models.ForeignKey(Prefactor, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField('requests/prefactors/verifications/')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Payment(models.Model):
    xpref_id = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    number = models.IntegerField()
    amount = models.FloatField()
    image = models.ImageField('request/payments/')
    payment_date = models.DateTimeField(default=now)
    summary = models.TextField(max_length=600, blank=True, null=True)

    def pub_date_pretty(self):
        return self.payment_date.strftime('%b %e %Y')

