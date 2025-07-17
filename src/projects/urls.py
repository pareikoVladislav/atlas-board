from django.urls import path, include
from src.projects.views import create_new_project, update_project, get_all_projects
from src.projects.urls import task as task_urls

urlpatterns = [
    path('', get_all_projects, name='get_all_projects'),
    path('create/', create_new_project, name='create_new_project'),
    path('<int:project_id>/update/', update_project, name='update_by_id'),

    path('tasks/', include(task_urls)),
]
