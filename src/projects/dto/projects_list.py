from rest_framework import serializers
from src.projects.models.project import Project


class ProjectsListDTO(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'start_date',
            'status',
            'is_active',
            'priority',
        ]
