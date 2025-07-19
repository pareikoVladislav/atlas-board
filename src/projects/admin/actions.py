from django.contrib import messages, admin
from src.choices.task import Status, Priority


@admin.action(description='Mark selected tasks as In Progress')
def mark_as_in_progress(modeladmin, request, queryset):
    """Mark selected tasks as In Progress"""
    updated_count = queryset.update(status='in_progress')
    messages.success(
        request,
        f'Successfully marked {updated_count} task(s) as In Progress.'
    )


@admin.action(description='Mark selected tasks as Completed')
def mark_as_completed(modeladmin, request, queryset):
    """Mark selected tasks as Completed"""
    updated_count = queryset.update(status='done')
    messages.success(
        request,
        f'Successfully marked {updated_count} task(s) as Completed.'
    )


@admin.action(description='Set high priority for selected tasks')
def set_high_priority(modeladmin, request, queryset):
    """Set selected tasks as High Priority"""
    updated_count = queryset.update(priority=Priority.HIGH.value[0])
    messages.success(
        request,
        f'Successfully set {updated_count} task(s) as High Priority.'
    )

