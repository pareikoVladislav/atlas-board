from src.projects.models.project import Project
from django.contrib import admin


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ...



