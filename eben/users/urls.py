from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'', views.UserViewSet, 'users')
router.register(r'user', views.UserView, 'user')
router.register(r'update', views.UserUpdateView, 'update')


urlpatterns = router.urls
