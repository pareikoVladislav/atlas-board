from django.urls import path, include

urlpatterns = [
    path('', include('src.projects.urls.project')),
    path('tags/', include('src.projects.urls.tag')),
    path('tasks/', include('src.projects.urls.task')),
    path('files/', include('src.projects.urls.project_file'))
]
