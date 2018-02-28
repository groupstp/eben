from rest_framework import viewsets, mixins

from .serializers import UserSerializer, UserUpdateSerializer
from .models import User


class UserView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Получение данных пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserUpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Редактирование пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'username'


class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка пользователей
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
