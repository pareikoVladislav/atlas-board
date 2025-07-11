from django.contrib import admin

from src.projects.models.task import Task
from .actions import mark_as_in_progress, mark_as_completed


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'project',
        'status',
        'priority',
        'assignee',
        'created_by',
        'deadline',
        'estimated_hours',
        'created_at'
    ]
    list_filter = [
        'status',
        'priority',
        'project',
        'created_at',
        'deadline',
        'assignee',
        'created_by',
    ]
    search_fields = [
        'title',
        'description',
        'project__name',
    ]
    ordering = ['-created_at']
    list_per_page = 25
    list_editable = [
        'status',
        'priority',
        'assignee'
    ]
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    actions = [mark_as_in_progress, mark_as_completed]
    fieldsets = (
        (
            "**Basic Information**", {
                "fields": ("title", "description", "project")
            }
        ),
        (
            "**Status & Priority**", {
                "fields": ("status", "priority"),
            }
        ),
        (
            "**Assignment**", {
                "fields": ("assignee", "created_by", "tags"),
            }
        ),
        (
            "**Timeline**", {
                "fields": ("deadline", "estimated_hours"),
            }
        ),
        (
            "**System Fields**", {
                "fields": ("created_at", "updated_at", "deleted_at"),
                "classes": ("collapse",)
            }
        ),
    )