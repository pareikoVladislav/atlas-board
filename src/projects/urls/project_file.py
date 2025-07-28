from django.urls import path

from src.projects.views import file_detail, FileProjectAPIView

urlpatterns = [
    path("<int:file_id>", file_detail, name="file detail"),
    path("", FileProjectAPIView.as_view(), name="project file create"),

]