import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    interest = models.CharField(max_length=100)
    last_request = models.DateTimeField(default=datetime.datetime(2022, 1, 1))


class Post(models.Model):
    topic = models.CharField(max_length=100)
    text = models.TextField()


class Like(models.Model):
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
