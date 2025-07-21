from rest_framework import serializers

from src.projects.models import ProjectFile
from src.users.dto import UserShortDTO

class ProjectFileDTO(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = (
            'id',
            'name',
            'file_path',
            'is_public',
        )


class CreateProjectFileDTO(serializers.ModelSerializer):

    class Meta:
        model = ProjectFile
        fields = (
            'name',
            'file_path',
            'uploaded_by'
        )



class ProjectFileDetailDTO(serializers.ModelSerializer):
    uploaded_by = UserShortDTO(read_only=True)

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

