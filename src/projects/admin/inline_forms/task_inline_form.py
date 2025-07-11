from django.contrib.admin import TabularInline

from src.projects.models import Task


class TaskInline(TabularInline):
    model = Task
    fields = [
        'title',
        'description',
        'status',
        'priority',
        'assignee',
        'deadline',
        'estimated_hours',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    extra = 1
    verbose_name = "Project Task"
    verbose_name_plural = "Project`s Tasks"