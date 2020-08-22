from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRelation(models.Model):
    parent = models.OneToOneField(User, related_name='user_parent', on_delete=models.CASCADE)
    child = models.ManyToManyField(User, related_name='user_child')

    def __str__(self):
        return f"parent: {self.parent}"
