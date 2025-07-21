from django.urls import path

from src.projects.views import file_detail

urlpatterns = [
    path("<int:file_id>", file_detail, name="file detail"),
]