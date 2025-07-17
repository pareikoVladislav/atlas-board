from django.urls import path
from src.projects.views import get_task_by_id, get_all_tasks

urlpatterns = [
    path('', get_all_tasks, name='get_all_tasks'),
    path('<int:task_id>/', get_task_by_id, name='get_task_by_id'),
]