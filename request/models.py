from django.db import models
import datetime
from django.utils.timezone import now


class Requests(models.Model):
    number = models.IntegerField()
    pub_date = models.DateTimeField(default=now)
    image = models.FileField('requests/')
    summary = models.TextField(max_length=1000)

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


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

