from django.urls import path, include

urlpatterns = [
    path('projects/', include('src.projects.urls')),
    path('users/', include('src.users.urls')),
]

