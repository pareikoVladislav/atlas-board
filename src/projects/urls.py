from django.urls import path
from src.projects.views.project_views import get_all_projects

urlpatterns = [
    path('projects/', get_all_projects, name='get_all_projects'),
]

