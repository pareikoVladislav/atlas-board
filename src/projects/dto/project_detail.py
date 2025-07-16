from rest_framework import serializers

from src.projects.models import Project

class ProjectDetailDTO(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
