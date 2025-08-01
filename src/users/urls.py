from django.urls import path
from src.users.views import retrieve_user, UserListGenericView

urlpatterns = [
    path('', UserListGenericView.as_view()),
    path('<int:user_id>/', retrieve_user),
]