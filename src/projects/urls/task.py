from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.projects.views.task import TaskViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='tasks')

# assign_to_me = TaskViewSet.as_view({'post': 'assign_to_me'})
# analytics_per_project = TaskViewSet.as_view({'get': 'analytics_per_project'})
# analytics_per_developer = TaskViewSet.as_view({'get': 'analytics_per_developer'})

urlpatterns = [
    path('', include(router.urls)),
    # path('<task_id>/assign_to_me/', assign_to_me, name='assign_to_me'),
    # path('analytics_per_project/', analytics_per_project, name='analytics_per_project'),
    # path('analytics_per_developer/', analytics_per_developer, name='analytics_per_developer'),
]


