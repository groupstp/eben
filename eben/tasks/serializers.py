from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'date_added', 'deadline',
                  'status', 'solution', 'solution_files',)
        read_only_field = ('status', 'id', 'date_added',
                           'solution', 'solution_files',)


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'status',)


class TaskSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'status', 'solution', 'solution_files',)
        read_only_field = ('id',)
