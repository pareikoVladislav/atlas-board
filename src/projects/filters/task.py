from django_filters import FilterSet, BooleanFilter
from src.projects.models import Task
from src.choices import Priority


class TaskFilter(FilterSet):
    unassigned_high_priority = BooleanFilter(method='filter_unassigned_high_priority')

    class Meta:
        model = Task
        fields = []

    def filter_unassigned_high_priority(self, queryset, name, value):
        if value:
            return queryset.filter(
                assignee__isnull=True,
                priority=Priority.HIGH.value[0]
            )
        return queryset