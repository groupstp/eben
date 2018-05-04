from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.UserViewList.as_view(),
        name='users'
    ),
    url(
        regex=r'^(?P<username>[a-zA-Z0-9]+)/$',
        view=views.UserView.as_view(),
        name='user'
    ),
    url(
        regex=r'^update/(?P<username>.+)/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    )
]
