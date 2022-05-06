from rest_framework import serializers

from core.models import MyUser, Post, Like


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    my_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

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


class MyUserActivitySerializer(serializers.Serializer):
    username = serializers.CharField()
    last_request = serializers.DateTimeField()
    last_login = serializers.DateTimeField()
