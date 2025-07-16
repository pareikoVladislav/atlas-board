from django.urls import path

from src.projects.views import update_project

urlpatterns = [
    path('/<int:project_id>/update/', update_project, name='update_by_id'),
]