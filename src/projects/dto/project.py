from typing import Any
from rest_framework.exceptions import ValidationError

from rest_framework import serializers

from src.projects.dto.task import NestedTaskShortInfoDTO
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

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        owner = attrs.get('owner')
        team_lead = attrs.get('team_lead')
        if owner.id == team_lead.id:
            raise ValidationError("The owner and team lead cannot be the same.")
        return attrs

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


class ProjectsListDetailDTO(serializers.ModelSerializer):
    tasks = NestedTaskShortInfoDTO(many=True)

    class Meta:
        model = Project
        fields = '__all__'
