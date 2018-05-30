from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response

from .models import Task
from .permissions import IsAuthor, IsDoer
from .serializers import TaskStatusSerializer, TaskSolutionSerializer, \
    TaskSerializer


class TaskAuthorViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                        mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, mixins.ListModelMixin):
    """
    Получение, создание,
    удаление(только если статус 'new'), обновление(только если статус 'new')
    задач(и)

    Только автор задачи
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthor,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'new':
            return super(TaskAuthorViewSet, self).update(request, *args,
                                                         **kwargs)
        else:
            return Response(_('Action not allowed'),
                            status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'new':
            # TODO: add notification to doer (Celery or Django Channels)
            return super(TaskAuthorViewSet, self).destroy(request, *args,
                                                          **kwargs)
        else:
            return Response(_('Action not allowed'),
                            status=status.HTTP_403_FORBIDDEN)


class TaskDoerViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin):
    """
    Получение задач(и)

    Только исполнитель задачи
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsDoer,)


class TaskAuthorStatusView(generics.UpdateAPIView, viewsets.GenericViewSet):
    """
    Изменение статуса задачи с 'verifying' на 'returned', 'done'

    Только автор задачи
    """
    queryset = Task.objects.all()
    serializer_class = TaskStatusSerializer
    permission_classes = (IsAuthor,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data['status'] in Task.STATUS_CHOICE[3:] and \
           instance.status == Task.STATUS_CHOICE[2][0]:

            data = {'status': request.data['status']}
        else:
            return Response(_('Action not allowed'),
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class TaskDoerSolutionView(generics.UpdateAPIView, viewsets.GenericViewSet):
    """
    Добавление решения задачи и(или)
    изменение статуса задача с 'new', 'doing', 'verifying'
    на 'doing', 'verifying'

    Только исполнитель задачи
    """
    queryset = Task.objects.all()
    serializer_class = TaskSolutionSerializer
    permission_classes = (IsDoer,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data['status'] in Task.STATUS_CHOICE[1:3][0] and \
           instance.status == Task.STATUS_CHOICE[0:3][0]:

            data = request.data
        else:
            return Response(_('Action not allowed'),
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
