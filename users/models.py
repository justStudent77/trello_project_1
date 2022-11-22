from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class TrelloUser(AbstractUser):
    boards = models.ManyToManyField(to="main.Board", null=True)
    archive = models.JSONField(default={})
    preferred = models.JSONField(default={})
    favourite = models.JSONField(default={})

    def __str__(self):
        return self.username







