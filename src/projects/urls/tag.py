from django.urls import path

from src.projects.views import delete_tag
from src.projects.views.tag import get_all_tags, create_tag, update_tag, get_tag_by_id

urlpatterns = [
    path('', get_all_tags, name='get_all_tags'),
    path('create/', create_tag, name='create_tag'),
    path('update/<int:tag_id>/', update_tag, name='update_tag'),
    path('delete/<int:tag_id>/', delete_tag, name='delete_tag'),
    path('<int:tag_id>/', get_tag_by_id, name='get_tag_by_id'),
]