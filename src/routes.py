from django.urls import path, include

urlpatterns = [
    path('projects/', include('src.projects.urls.project')),
    path('tasks/', include('src.projects.urls.task')),
]