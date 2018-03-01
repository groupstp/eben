from django.shortcuts import redirect
from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from .permissions import IsOwner
from .serializers import UserSerializer, UserUpdateSerializer
from .models import User


class UserView(generics.RetrieveAPIView):
    """
    Получение данных пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'username'


class UserViewList(generics.ListAPIView):
    """
    Получение списка пользователей
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer, ]


class UserUpdateView(generics.RetrieveUpdateAPIView):
    """
    Редактирование пользовательской информации
    """
    renderer_classes = [TemplateHTMLRenderer, ]
    template_name = 'users/user_form.html'
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserUpdateSerializer
    permission_classes = (IsOwner, )

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response({'serializer': serializer, type(instance).__name__: instance})

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, type(instance).__name__: instance})
        serializer.save()
        return redirect('ui')
