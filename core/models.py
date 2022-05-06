from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    last_request = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    text = models.TextField()
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Like(models.Model):
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

