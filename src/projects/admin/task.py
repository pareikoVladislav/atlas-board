from django.contrib import admin

from src.projects.models.task import Task


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


#
# ### При добавлении/редактировании объекта поля группировать:
# 1. **Basic Information**: `title` `description` `project`
# 2. **Status & Priority** `status` `priority`
# 3. **Assignment**: `assignee` `created_by` `tags`
# 4. **Timeline**: `due_date` `estimated_hours`
# 5. **System Fields** (только для чтения, сворачиваемые): `created_at` `updated_at` `deleted_at`
#
# ### Системные поля только для чтения:
# - `created_at`
# - `updated_at`
# - `deleted_at`


admin.site.register(Task, TaskAdmin)


