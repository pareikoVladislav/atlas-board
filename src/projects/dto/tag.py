from rest_framework import serializers

from src.projects.models import Tag

class TagBaseDTO(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name'
        ]


class TagCreateDTO(TagBaseDTO):
    pass


class TagUpdateDTO(TagBaseDTO):
    pass


class TagResponseDTO(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
