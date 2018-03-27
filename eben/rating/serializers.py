from eben.users.serializers import UserSerializer
from .models import AllRating, Rating, HistoryRating, CategoryRating
from rest_framework import serializers


class AllRatingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для полного рейтинга. Выдает пользователя и текущий рейтинг.
    """
    user = UserSerializer()

    class Meta:
        model = AllRating
        fields = ('user', 'all_rating', )


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    class Meta:
        model = CategoryRating
        fields = ('category', )


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для рейтинга по категории. Выдает ссылку на полный рейтинг, категорию и текущий рейтинг.
    """
    rating = AllRatingSerializer()
    category = CategorySerializer()

    class Meta:
        model = Rating
        fields = ('rating', 'category', 'current_rating', )


class HistoryRatingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для истории изменения рейтинга.
    Выдает ссылку на рейтинг по категории, описание действия изменившего рейтинг,
    значения изменения и время изменения
    """
    rating = RatingSerializer()

    class Meta:
        model = HistoryRating
        fields = ('rating', 'action', 'value', 'date_time', )
