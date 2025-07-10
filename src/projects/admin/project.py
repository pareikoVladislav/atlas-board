from src.projects.models.project import Project
from django.contrib import admin


class ProjectAdmin(admin.ModelAdmin):
    ...

admin.site.register(Project, ProjectAdmin)

