from django.contrib.auth.models import User
from django.db import models
import datetime
from django.utils.timezone import now
from customer.models import Customer


class Requests(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.FileField(upload_to='requests/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class ReqSpec(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
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
    images = models.FileField(upload_to='specs/')
    summary = models.TextField(max_length=500, blank=True, null=True)


class Xpref(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    req_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='prefactors/')

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class PrefSpec(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
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
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    xpref = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='verifications/')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Prefactor(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    request_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='prefactors')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class PrefactorVerification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    pref_id = models.ForeignKey(Prefactor, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='pref_verifications')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Permission(models.Model):
    proforma = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Payment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    xpref_id = models.ForeignKey(Xpref, on_delete=models.CASCADE)
    number = models.IntegerField()
    amount = models.FloatField()
    image = models.ImageField(upload_to='payments/', default='payments/default.jpg')
    payment_date = models.DateTimeField(default=now)
    summary = models.TextField(max_length=600, blank=True, null=True)

    def pub_date_pretty(self):
        return self.payment_date.strftime('%b %e %Y')

