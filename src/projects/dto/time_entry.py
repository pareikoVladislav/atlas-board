from typing import Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.projects.models import TimeEntry


class TimeEntryCreateDTO(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = '__all__'

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        hours = attrs.get('hours')
        if hours > 50:
            raise ValidationError("Task can not take more than 50 hours")
        return attrs


class TimeEntryDTO(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = '__all__'
