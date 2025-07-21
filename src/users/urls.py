from django.urls import path
from src.users.views import retrieve_user, get_all_users

urlpatterns = [
    path('', get_all_users),
    path('<int:user_id>/', retrieve_user),
]