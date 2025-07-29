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

class TaskAnalyticsPerProjectDTO(serializers.Serializer):
    project_id = serializers.IntegerField()
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    urgent_tasks_count = serializers.IntegerField()

class TaskAnalyticsPerDeveloperDTO(serializers.Serializer):
    assignee_id = serializers.IntegerField(allow_null=True)
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    urgent_tasks_count = serializers.IntegerField()
