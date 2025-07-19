from django.urls import path
from src.projects.views import task_list, task_detail

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:task_id>/', task_detail, name='task_detail'),
]
