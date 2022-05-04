from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from core.models import MyUser, Post, Like


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'password', 'interest')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validate_password(validated_data['password'])
        user = MyUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            interest=validated_data['interest'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class AnalyticSerializer(serializers.Serializer):
    day = serializers.DateTimeField()
    count = serializers.IntegerField()
