from django.db import models
from prefactor.models import PreFactor

class PrefactorVerification(models.Model):
    pref_ver_id = models.IntegerField()
    PreFactor_Id = models.IntegerField()
    pref_ver_Image = models.ImageField(upload_to='pref_verification/')
    pref_summary = models.TextField(max_length=600)

