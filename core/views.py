from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from core.models import MyUser
from core.serializers import UserSerializer


class UserRegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


# class UserList(viewsets.ModelViewSet):
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser, ]
#
#     @action(detail=True, methods=['get'])
#     def ll(self, request: Request, pk):
#         return Response(self.get_object().last_login)
