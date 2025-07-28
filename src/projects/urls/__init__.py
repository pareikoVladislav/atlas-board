from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.projects.views.task import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include('src.projects.urls.project')),
    path('tags/', include('src.projects.urls.tag')),
    path('files/', include('src.projects.urls.project_file')),
] + router.urls
