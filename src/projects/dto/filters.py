from rest_framework import serializers

from src.choices.common import Priority
from src.choices.project import ProjectStatus


class ProjectFilterDTO(serializers.Serializer):
    owner_username = serializers.CharField(required=False)
    members_count_from = serializers.IntegerField(required=False, min_value=0)
    members_count_to = serializers.IntegerField(required=False, min_value=0)
    start_date_from = serializers.DateField(required=False)
    start_date_to = serializers.DateField(required=False)
    status = serializers.ChoiceField(required=False, choices=ProjectStatus.choices())
    priority = serializers.ChoiceField(required=False, choices=Priority.choices())
    ordering = serializers.ChoiceField(
        required=False,
        choices=[
            'priority', '-priority',
            'start_date', '-start_date',
            'end_date', '-end_date',
        ]
    )

    def validate(self, data):
        errors = {}

        if data.get("start_date_from") and data.get("start_date_to"):
            if data["start_date_from"] > data["start_date_to"]:
                errors["start_date"] = ["start_date_from must be before start_date_to"]

        if data.get("members_count_from") and data.get("members_count_to"):
            if data["members_count_from"] > data["members_count_to"]:
                errors["members_count"] = ["members_count_from must be <= members_count_to"]

        if errors:
            raise serializers.ValidationError(errors)

        return data