from django.urls import path

from src.projects.views import create_task, update_task, delete_task

urlpatterns = [
    path('create/', create_task, name='create_task'),
    path('<int:task_id>/update/', update_task, name='update_task'),
    path('<int:task_id>/delete/', delete_task, name='delete_task'),
]