from django.db import models


class Requests(models.Model):
    number = models.IntegerField()
    image = models.FileField('requests/')
    summary = models.TextField(max_length=1000)


class Prefactor(models.Model):
    request_id = models.ForeignKey(Requests, on_delete=models.CASCADE)
    number = models.IntegerField()
    image = models.ImageField('requests/prefactors/original/')
    summary = models.TextField(max_length=1000)


class PrefactorVerification(models.Model):
    pref_id = models.ForeignKey(Prefactor, on_delete=models.CASCADE)
    number = models.IntegerField()
    image = models.ImageField('requests/prefactors/verifications/')
    summary = models.TextField(max_length=1000)

