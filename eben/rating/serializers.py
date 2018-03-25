from .models import AllRating, Rating, HistoryRating
from rest_framework import serializers


class AllRatingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для полного рейтинга. Выдает пользователя и текущий рейтинг.
    """
    class Meta:
        model = AllRating
        fields = ('user', 'all_rating', )


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для рейтинга по категории. Выдает ссылку на полный рейтинг, категорию и текущий рейтинг.
    """
    class Meta:
        model = Rating
        fields = ('rating', 'category', 'current_rating', )


class HistoryRatingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для истории изменения рейтинга.
    Выдает ссылку на рейтинг по категории, описание действия изменившего рейтинг,
    значения изменения и время изменения
    """
    class Meta:
        model = HistoryRating
        fields = ('rating', 'action', 'value', 'date_time', )
