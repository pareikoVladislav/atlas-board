from django.urls import path
from src.projects.views import create_new_project, update_project, get_all_projects

urlpatterns = [
    path('', get_all_projects, name='get_all_projects'),
    path('create/', create_new_project, name='create_new_project'),
    path('update/<int:project_id>/', update_project, name='update_by_id'),
]