from eben.users.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для получения данных пользователя
    """
    class Meta:
        model = User
        fields = ('name', 'first_name', 'last_name', 'avatar', 'date_of_birth', 'info', 'username', )

class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для редактирования данных пользователя
    """
    class Meta:
        model = User
        fields = ('name', 'first_name', 'last_name', 'avatar', 'date_of_birth', 'info', )
