from rest_framework import generics, permissions, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer

from .serializers import RatingSerializer, AllRatingSerializer, HistoryRatingSerializer, CategorySerializer

from .models import AllRating, Rating, HistoryRating, CategoryRating


class MultipleFieldsView(generics.GenericAPIView):
    """
    Вспомогательное представление для поиска объекта(объектов) по нескольким полям.
    """

    # Для поиска через отношения с другими моделями нужно указывать путь к полю по которому нужно делать поиск.
    # Например 'model__field', где model это поле в модели которую нужно получить, а field поле по которому будет поиск.
    lookup_fields = ['pk', ]
    # Каждый элемент массива это имя моля по которому будет идти поиск.
    lookup_url_kwargs = ['pk', ]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwargs = self.lookup_url_kwargs or self.lookup_fields

        filter_kwargs = {}
        for i in range(len(self.lookup_fields)):
            assert lookup_url_kwargs[i] in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwargs[i])
            )
            filter_kwargs[self.lookup_fields[i]] = self.kwargs[lookup_url_kwargs[i]]

        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class AllRatingDetail(generics.RetrieveAPIView):
    """
    Получение полного рейтинга пользователя.
    """
    queryset = AllRating.objects.all()
    serializer_class = AllRatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
    permission_classes = [permissions.IsAuthenticated, ]


class RatingList(generics.ListAPIView):
    """
    Получение списка рейтинга одного пользователя по всем категориям.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'rating__user__username'
    lookup_url_kwarg = 'username'
    permission_classes = [permissions.IsAuthenticated, ]


class RatingCategoryList(generics.ListAPIView):
    """
    Получение списка рейтинга одной категории по всем пользователям.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'category__category'
    lookup_url_kwarg = 'category'
    permission_classes = [permissions.IsAuthenticated, ]


class RatingDetail(MultipleFieldsView, mixins.RetrieveModelMixin):
    """
    Получение рейтинга пользователя по одной категории
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = [JSONRenderer, ]
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_fields = ['rating__user__username', 'category__category', ]
    lookup_url_kwargs = ['username', 'category', ]


class CategoryDetail(generics.RetrieveAPIView):
    """
    Вспомогательное представление для рейтинга по категориям. Выводит только название категории.
    """
    queryset = CategoryRating.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'category'
    permission_classes = [permissions.IsAuthenticated, ]


class HistoryList(generics.ListAPIView):
    """
    Получение истории рейтинга одного пользователя.
    """
    queryset = HistoryRating.objects.all()
    serializer_class = HistoryRatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_field = 'rating'
    permission_classes = [permissions.IsAuthenticated, ]


class HistoryCategoryList(MultipleFieldsView, mixins.ListModelMixin):
    """
    Получение истории рейтинга одного пользователя по одной категории.
    """
    queryset = HistoryRating.objects.all()
    serializer_class = HistoryRatingSerializer
    renderer_classes = [JSONRenderer, ]
    lookup_fields = ['rating__rating__user__username', 'rating__category__category', ]
    lookup_url_kwargs = ['username', 'category', ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
