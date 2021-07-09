from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    balance = models.IntegerField(default=200_000)
