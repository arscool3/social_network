from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    interest = models.CharField(max_length=100)
    last_request = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    topic = models.CharField(max_length=100)
    text = models.TextField()
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Like(models.Model):
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BotFactory(models.Model):
    number_of_users = models.IntegerField()
    max_posts = models.IntegerField()
    max_likes = models.IntegerField()