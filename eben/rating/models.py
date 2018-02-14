from django.db import models
from django.utils.translation import ugettext_lazy as _


class AllRating(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    all_rating = models.IntegerField


class CategoryRating(models.Model):
    category = models.CharField


class Rating(models.Model):
    rating = models.ForeignKey(AllRating, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryRating, on_delete=models.CASCADE)
    current_rating = models.IntegerField


class HistoryRating(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    action = models.CharField
    value = models.IntegerField(editable=False)
    date_time = models.DateTimeField(auto_now_add=True)
