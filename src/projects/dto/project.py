from rest_framework import serializers
from src.projects.models import Project


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


class ProjectCreateDTO(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'owner',
            'team_lead',
            'status',
            'is_active',
            'priority'
        ]

class ProjectDetailDTO(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = [
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted'
        ]

class ProjectUpdateDTO(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'team_lead',
            'start_date',
            'end_date',
            'status',
            'is_active',
            'priority',
        )
