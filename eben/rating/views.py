from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer

from .serializers import RatingSerializer, AllRatingSerializer, HistoryRatingSerializer

from .models import AllRating, Rating, HistoryRating


class AllRatingDetail(generics.RetrieveAPIView):
    """
    Получение полного рейтинга пользователя
    """
    queryset = AllRating.objects.all()
    serializer_class = AllRatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'user.username'
    permission_classes = permissions.IsAuthenticated


class RatingList(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'rating'
    permission_classes = permissions.IsAuthenticated


class RatingCategoryList(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'category'
    permission_classes = permissions.IsAuthenticated


class RatingDetail(generics.RetrieveAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    permission_classes = permissions.IsAuthenticated


class HistoryList(generics.ListAPIView):
    queryset = HistoryRating.objects.all()
    serializer_class = HistoryRatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'rating'
    permission_classes = permissions.IsAuthenticated
