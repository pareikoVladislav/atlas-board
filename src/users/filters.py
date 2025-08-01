import django_filters
from django.db.models import Count

from src.users.models import User


class UserFilter(django_filters.FilterSet):
    project_name = django_filters.CharFilter(
        field_name='main_project__name',
        lookup_expr='icontains',
        label='Project name'
    )
    tasks_from = django_filters.NumberFilter(
        method='filter_by_tasks_from',
        label='Task from'
    )
    tasks_to = django_filters.NumberFilter(
        method='filter_by_tasks_to',
        label='Task to'
    )

    class Meta:
        model = User
        fields = []

    def filter_by_tasks_from(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.annotate(
            count_tasks=Count('main_project__tasks', distinct=True)
        ).filter(count_tasks__gte=value)

    def filter_by_tasks_to(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.annotate(
            count_tasks=Count('main_project__tasks', distinct=True)
        ).filter(count_tasks__lte=value)
