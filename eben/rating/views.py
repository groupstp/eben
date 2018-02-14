from django.http import Http404
from django.views.generic import DetailView, ListView
from django.utils.translation import ugettext as _

from .models import AllRating, Rating


class AllRatingDetail(DetailView):
    model = AllRating
    slug_field = 'user.username'
    slug_url_kwarg = 'user.username'


class RatingList(ListView):
    model = Rating
    slug_field = 'rating' + AllRatingDetail.slug_field
    slug_url_kwarg = 'rating' + AllRatingDetail.slug_url_kwarg


class RatingDetail(DetailView):
    model = Rating
    slug_field = 'rating' + AllRatingDetail.slug_field
    slug_url_kwarg = 'rating' + AllRatingDetail.slug_url_kwarg

    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs.get(self.slug_url_kwarg)
        category = self.kwargs.get(self.slug_url_kwarg)
        if category is not None:
            queryset = queryset.filter(**{category: category})
        if username is not None:
            queryset = queryset.filter(**{username: username})
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
