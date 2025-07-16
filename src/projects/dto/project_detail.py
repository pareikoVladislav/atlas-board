from rest_framework import serializers

from src.projects.models import Project

class ProjectDetailDTO(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = (
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted'
        )
