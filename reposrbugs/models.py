from django.db import models
from accounts.models import User
# Create your models here.


class Bugs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    suggestion = models.TextField(max_length=1000, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
