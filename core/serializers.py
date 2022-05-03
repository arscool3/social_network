from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password

from core.models import MyUser


class UserSerializer(ModelSerializer):
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
