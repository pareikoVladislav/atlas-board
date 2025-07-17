from django.urls import path
from src.users.views import get_by_id, get_all_users

urlpatterns = [
    path('', get_all_users, name='get_all_users'),
    path('<int:user_id>/', get_by_id, name='get_by_id'),
]