from rest_framework import serializers

from src.projects.models import ProjectFile
from src.users.dto import UserShortSerializer

class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = (
            'id',
            'name',
            'file_path',
            'is_public',
        )



class ProjectFileDetailSerializer(serializers.ModelSerializer):
    uploaded_by = UserShortSerializer(read_only=True)

    class Meta:
        model = ProjectFile
        fields = (
            'id',
            'name',
            'file_path',
            'is_public',
            'uploaded_by',
            'created_at',
        )

