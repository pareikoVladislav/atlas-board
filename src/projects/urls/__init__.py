from django.urls import path, include

urlpatterns = [
    path('', include('src.projects.urls.project')),
    path('tags/', include('src.projects.urls.tag'))
]