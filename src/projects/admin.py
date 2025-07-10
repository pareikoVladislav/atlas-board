from django.contrib import admin

from src.projects.models.project import Project


@admin.register
class ProjectAdmin(admin.ModelAdmin):
    model = Project