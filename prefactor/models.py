from django.db import models


class PreFactor(models.Model):
    PreFactor_Id = models.IntegerField()
    Summary = models.TextField(max_length=600)
    Image = models.ImageField(upload_to='prefactor/')

