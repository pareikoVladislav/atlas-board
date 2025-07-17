from rest_framework import serializers
from src.users.models import User


class ProjectsListDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
        ]

class ProjectDetailDTO(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'updated_at',
            'deleted_at',
            'deleted'
        ]
