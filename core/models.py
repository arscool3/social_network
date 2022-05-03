import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    interest = models.CharField(max_length=100)
    last_request = models.DateTimeField(default=datetime.datetime(2022, 1, 1))
