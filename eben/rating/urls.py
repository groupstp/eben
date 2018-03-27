from django.conf.urls import url

from .views import (
    AllRatingDetail,
    RatingCategoryList,
    RatingList,
    RatingDetail,
    HistoryList,
    HistoryCategoryList,
    CategoryDetail,
)

urlpatterns = [
    url(
        regex=r'^(?P<username>[a-zA-Z0-9]+)/$',
        view=AllRatingDetail.as_view(),
        name='all'
    ),
    url(
        regex=r'^category_rating/(?P<category>[a-zA-Z0-9]+)/$',
        view=RatingCategoryList.as_view(),
        name='category_rating'
    ),
    url(
        regex=r'^list/(?P<username>[a-zA-Z0-9]+)/$',
        view=RatingList.as_view(),
        name='list'
    ),
    url(
        regex=r'^detail/(?P<username>[a-zA-Z0-9]+)/(?P<category>[a-zA-Z0-9]+)/$',
        view=RatingDetail.as_view(),
        name='detail'
    ),
    url(
        regex=r'^category/(?P<category>[a-zA-Z0-9]+)/$',
        view=CategoryDetail.as_view(),
        name='category'
    ),
    url(
        regex=r'^history/(?P<username>[a-zA-Z0-9]+)/$',
        view=HistoryList.as_view(),
        name='history'
    ),
    url(
        regex=r'^history/(?P<username>[a-zA-Z0-9]+)/(?P<category>[a-zA-Z0-9]+)/$',
        view=HistoryCategoryList.as_view(),
        name='history'
    ),
]
