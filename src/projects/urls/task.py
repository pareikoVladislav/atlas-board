from django.urls import path
from src.projects.views import task_list, task_detail, analytics_per_project, analytics_per_developer
from src.projects.views.task import TaskCommentsAPIView, TaskCommentDetailAPIView

urlpatterns = [
    path('', task_list, name='task_list'),
    path('analytics_per_project/', analytics_per_project, name='analytics_per_project'),
    path('analytics_per_developer/', analytics_per_developer, name='analytics_per_developer'),
    path('<int:task_id>/', task_detail, name='task_detail'),
    path('<int:task_id>/comments/', TaskCommentsAPIView.as_view(), name='task_comments'),
    path('<int:task_id>/comments/<int:comment_id>/', TaskCommentDetailAPIView.as_view(), name='task_comment_detail'),
]
