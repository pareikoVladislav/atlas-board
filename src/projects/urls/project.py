from django.urls import path, include

from src.projects.views import (
    create_new_project,
    update_project,
    get_all_projects,
    get_all_project_files

)

urlpatterns = [
    path('', get_all_projects, name='get_all_projects'),
    path('create/', create_new_project, name='create_new_project'),
    path('update/<int:project_id>/', update_project, name='update_by_id'),
    path('<int:project_id>/files/', get_all_project_files, name='get_all_project_files'),
]
