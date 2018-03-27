from django.contrib import admin

from .models import AllRating, Rating, CategoryRating, HistoryRating


@admin.register(AllRating)
class AllRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryRating)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(HistoryRating)
class HistoryAdmin(admin.ModelAdmin):
    pass
