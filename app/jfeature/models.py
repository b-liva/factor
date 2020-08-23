from django.db import models
from django.contrib.auth import get_user_model
from request.models import TimeStampedModel
User = get_user_model()
# Create your models here.


class Feature(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    done = models.BooleanField(default=False)
    done_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.owner.last_name}: {self.title}"
