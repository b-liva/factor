from django.db import models
from accounts.models import User
from request.models import ReqSpec
# Create your models here.


class SpecCommunications(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField(max_length=1000)
    spec = models.ForeignKey(ReqSpec, on_delete=models.DO_NOTHING)
    is_read = models.BooleanField(default=False)
