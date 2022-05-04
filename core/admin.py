from django.contrib import admin
from .models import MyUser, Post, Like

admin.site.register(MyUser)
admin.site.register(Post)
admin.site.register(Like)
