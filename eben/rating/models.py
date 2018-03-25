from django.db import models
from django.utils.translation import ugettext_lazy as _


class AllRating(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    all_rating = models.IntegerField(_("Full rating of User"))


class CategoryRating(models.Model):
    category = models.CharField(_("Name of category"), max_length=120)


class Rating(models.Model):
    rating = models.ForeignKey(AllRating, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryRating, on_delete=models.CASCADE)
    current_rating = models.IntegerField(_("Rating of User by category"))


class HistoryRating(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    action = models.CharField(_("Action that changed the rating"), max_length=120)
    value = models.IntegerField(_("Value on which the rating has changed"), editable=False)
    date_time = models.DateTimeField(_("Time of rating change"), auto_now_add=True)
