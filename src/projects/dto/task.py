from django.core.exceptions import ValidationError
from rest_framework import serializers
from src.projects.models import Task, TaskComment


class TaskCommentCreateDTO(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['text']

    def create(self, validated_data):
        # Получаем task_id из URL
        task_id = self.context['view'].kwargs.get('task_id')
        author = self.context['request'].user

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ValidationError("Task not found")

        # Упрощенная проверка доступа - можно расширить позже
        # Пока что любой аутентифицированный пользователь может комментировать

        return TaskComment.objects.create(
            task=task,
            author=author,
            **validated_data
        )

class TaskCommentDeleteDTO(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['id']

class TaskCommentDetailDTO(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.CharField(source='author.email', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

class TaskCommentUpdateDTO(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['text']


class TaskCommentListDTO(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.CharField(source='author.email', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = TaskComment
        fields = [
            'id',
            'text',
            'author',
            'author_username',
            'author_email',
            'created_by_username',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_by', 'created_at', 'updated_at']


class TasksListDTO(serializers.ModelSerializer):
    # Добавляем читаемые поля из связанных объектов
    project_name = serializers.CharField(source='project.name', read_only=True)
    assignee_username = serializers.CharField(source='assignee.username', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'estimated_hours',
            'deadline',
            'project',          # ID проекта
            'project_name',     # Название проекта
            'assignee',         # ID исполнителя
            'assignee_username', # Имя исполнителя
            'created_by',       # ID создателя
            'created_by_username', # Имя создателя
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
