from rest_framework.routers import SimpleRouter

from .views import TaskAuthorViewSet, TaskDoerViewSet, TaskAuthorStatusView, \
    TaskDoerSolutionView

router = SimpleRouter()
router.register(r'author', TaskAuthorViewSet, 'author')
router.register(r'doer', TaskDoerViewSet, 'doer')
router.register(r'status', TaskAuthorStatusView, 'status')
router.register(r'solution', TaskDoerSolutionView, 'solution')

urlpatterns = [] + router.urls
