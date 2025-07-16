from django.urls import path

from src.projects.views import (
    update_project,
    get_all_projects
)

urlpatterns = [
    path('/<int:project_id>/update/', update_project, name='update_by_id'),
    path('', get_all_projects, name='get_all_projects'),
]