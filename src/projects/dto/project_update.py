from rest_framework import serializers

from src.projects.models import Project

class ProjectUpdateDTO(serializers.ModelSerializer):
    partial = True
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
