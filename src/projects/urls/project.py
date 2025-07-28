from django.urls import path

from src.projects.views import (
    create_new_project,
    update_project,
    get_all_projects,
    get_all_project_files

)
from src.projects.views.project import get_active_projects

urlpatterns = [
    path('', get_all_projects, name='get_all_projects'),
    path('extended/', get_active_projects, name='get_active_projects'),
    path('create/', create_new_project, name='create_new_project'),
    path('update/<int:project_id>/', update_project, name='update_by_id'),
    path('<int:project_id>/files/', get_all_project_files, name='get_all_project_files'),
]
