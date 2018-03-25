from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer

from .serializers import RatingSerializer, AllRatingSerializer, HistoryRatingSerializer

from .models import AllRating, Rating, HistoryRating


class AllRatingDetail(generics.RetrieveAPIView):
    """
    Получение полного рейтинга пользователя.
    """
    queryset = AllRating.objects.all()
    serializer_class = AllRatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'user.username'
    permission_classes = permissions.IsAuthenticated


class RatingList(generics.ListAPIView):
    """
    Получение списка рейтинга одного пользователя по всем категориям.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'rating'
    permission_classes = permissions.IsAuthenticated


class RatingCategoryList(generics.ListAPIView):
    """
    Получение списка рейтинга одной категории по всем пользователям.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'category'
    permission_classes = permissions.IsAuthenticated


class RatingDetail(generics.RetrieveAPIView):
    """
    Получение рейтинга пользователя по одной категории
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    permission_classes = permissions.IsAuthenticated


class HistoryList(generics.ListAPIView):
    """
    Получение истории рейтинга одного пользователя.
    """
    queryset = HistoryRating.objects.all()
    serializer_class = HistoryRatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'rating'
    permission_classes = permissions.IsAuthenticated
