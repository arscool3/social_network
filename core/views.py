import datetime

from django.db.models import functions, Count
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from core.models import Post, MyUser, Like
from core.serializers import (
    MyUserSerializer, PostSerializer, LikeSerializer, AnalyticSerializer, MyUserActivitySerializer
)
from core.permissions import MyUserPermission


class MyUserRegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=['post'])
    def like(self, request: Request, pk: int):
        serializer = LikeSerializer(data=dict(my_user=request.user.id, post=pk))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def unlike(self, request: Request, pk: int):
        Like.objects.filter(my_user=request.user.id, post=pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=False, methods=['get'])
    def analytics(self, request: Request):
        try:
            date_from = request.query_params['date_from']
            date_to = request.query_params['date_to']
        except:
            return Response('No date were provided', status=HTTP_400_BAD_REQUEST)

        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

        analytics = Like.objects \
            .filter(created_at__gte=date_from, created_at__lte=date_to) \
            .annotate(day=functions.TruncDay('created_at')) \
            .values('day').annotate(count=Count('id')).values('day', 'count')

        serializer = AnalyticSerializer(analytics, many=True)

        return Response(serializer.data)


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [MyUserPermission, ]

    @action(detail=True, methods=['get'])
    def activity(self, request: Request, pk: int):
        try:
            user = MyUser.objects.filter(id=pk)[0]
        except:
            return Response('No users with given parameters', status=HTTP_400_BAD_REQUEST)
        serializer = MyUserActivitySerializer(data=dict(username=user.username,
                                                        last_request=user.last_request,
                                                        last_login=user.last_login))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class BotView(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        pass
