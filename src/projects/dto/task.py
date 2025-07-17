from rest_framework import serializers
from src.projects.models import Task

class TasksListDTO(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'estimated_hours',
            'deadline',
            'project',
            'assignee',
            'created_by',
            'tags',
        ]


class TaskDetailDTO(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'estimated_hours',
            'deadline',
            'project',
            'assignee',
            'created_by',
            'tags',
        ]

class TaskCreateDTO(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'estimated_hours',
            'deadline',
            'project',
            'assignee',
            'created_by',
            'tags',
        ]

class TaskUpdateDTO(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'deadline',
            'estimated_hours',
            'tags',
        ]