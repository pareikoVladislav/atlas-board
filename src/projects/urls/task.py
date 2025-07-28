from django.urls import path
from src.projects.views import (
    task_list,
    task_detail,
    analytics_per_project,
    analytics_per_developer,
    create_time_entry
)

urlpatterns = [
    path('', task_list, name='task_list'),
    path('time-entries/', create_time_entry, name='create_time_entry'),
    path('analytics_per_project/', analytics_per_project, name='analytics_per_project'),
    path('analytics_per_developer/', analytics_per_developer, name='analytics_per_developer'),
    path('<int:task_id>/', task_detail, name='task_detail'),
]
