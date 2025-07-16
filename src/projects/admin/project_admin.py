from django.contrib import admin

from src.projects.models.project import Project

from src.projects.admin.inline_forms import TaskInline


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInline]
    # Отображаемые поля в списке
    list_display = (
        'name',
        'status',
        'start_date',
        'owner',
        'description',
        'created_at',
        'end_date'
    )
    # Поля фильтрации
    list_filter = (
        'status',
        'start_date',
        'owner',
        'created_at',
        'end_date',
    )
    # Поля поиска
    search_fields = (
        'name',
        'description',
        'owner__first_name',
        'owner__last_name',
    )
    # Сортировка: новые проекты сверху
    ordering = ('-created_at',)
    # Количество объектов на странице
    list_per_page = 20
    # Быстрое редактирование
    list_editable = ('status', 'owner')
    # Группировка полей в форме добавления/редактирования
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'owner')
        }),
        ('Status & Timeline', {
            'fields': ('status', 'start_date', 'end_date')
        }),
        # ('Files', {
        #     'fields': ('files',),
        # }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',),
        }),
    )

    # Только для чтения
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')