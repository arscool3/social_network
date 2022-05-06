import datetime

from django.db.models import functions, Count
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from celery.result import AsyncResult

from core.models import Post, MyUser, Like, BotFactory
from core.serializers import (
    MyUserSerializer,
    PostSerializer,
    LikeSerializer,
    AnalyticSerializer,
    MyUserActivitySerializer,
    BotFactorySerializer,
)
from core.permissions import MyUserPermission
from core.tasks import bot_factory_task


class MyUserRegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
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
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, ]

    @action(detail=False, methods=['get'])
    def analytics(self, request: Request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        if date_from is None or date_to is None:
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
    pagination_class = PageNumberPagination
    permission_classes = [MyUserPermission, ]

    @action(detail=True, methods=['get'])
    def activity(self, request: Request, pk: int):
        user = MyUser.objects.filter(id=pk)
        if len(user) == 0:
            return Response('No users with given parameters', status=HTTP_400_BAD_REQUEST)

        serializer = MyUserActivitySerializer(data=dict(username=user.username,
                                                        last_request=user.last_request,
                                                        last_login=user.last_login))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class BotFactoryViewSet(viewsets.ModelViewSet):
    queryset = BotFactory.objects.all()
    serializer_class = BotFactorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser, ]

    def create(self, request, *args, **kwargs):
        web_url = f"http://{request.get_host()}"

        try:
            number_of_users = int(request.data['number_of_users'])
            max_posts_per_user = int(request.data['max_posts_per_user'])
            max_likes_per_user = int(request.data['max_likes_per_user'])
        except:
            return Response('No date were provided', status=HTTP_400_BAD_REQUEST)

        task = bot_factory_task.delay(web_url, number_of_users, max_posts_per_user, max_likes_per_user)

        serializer = BotFactorySerializer(data=dict(number_of_users=number_of_users,
                                                    max_posts=max_posts_per_user,
                                                    max_likes=max_likes_per_user))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(task.id)

    @action(detail=False, methods=['get'])
    def status(self, request: Request):
        task_id = request.query_params.get('task_id')
        if task_id:
            return Response({'status': f'{AsyncResult(task_id).status}'})
        return Response('No task id is provided')
