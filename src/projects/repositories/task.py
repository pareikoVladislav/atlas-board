from datetime import timedelta
from typing import Any

from django.db.models import Count, Case, When, IntegerField, Q
from django.utils import timezone
from django.db.models.query import QuerySet
from django.db import DatabaseError, OperationalError

from src.choices import Status
from src.projects.models import Task
from src.projects.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    def __init__(self):
        super().__init__(Task)

    def get_all(self) -> QuerySet:
        """
        Получить все задачи с предзагрузкой связанных данных
        """
        try:
            qs = self.model.objects.select_related(
                'project',  # JOIN с таблицей projects
                'assignee',  # JOIN с таблицей users (assignee)
                'created_by'  # JOIN с таблицей users (created_by)
            ).prefetch_related(
                'tags'  # Отдельный запрос для ManyToMany связи
            )
            return qs
        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve {self.model.__name__} objects') from e

    def get_tasks_analytics_per_project(self) -> QuerySet[dict[str, Any]]:
        try:
            queryset = self.model.objects.values('project_id').annotate(
                total_tasks=Count('id'),
                completed_tasks=Count(Case(
                    When(status=Status.done, then=1),
                    output_field=IntegerField()
                )),
                urgent_tasks_count=Count(
                    Case(
                        When(
                            Q(status__in=[Status.in_progress, Status.pending]) &
                            Q(deadline__lte=timezone.now() + timedelta(days=5)) &
                            Q(deadline__gte=timezone.now()),
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                )
            )
            return queryset

        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve data') from e

    def get_tasks_analytics_per_developer(self) -> QuerySet[dict[str, Any]]:
        try:
            queryset = self.model.objects.values('assignee_id').annotate(
                total_tasks=Count('id'),
                completed_tasks=Count(Case(
                    When(status=Status.done, then=1),
                    output_field=IntegerField()
                )),
                urgent_tasks_count=Count(
                    Case(
                        When(
                            Q(status__in=[Status.in_progress, Status.pending]) &
                            Q(deadline__lte=timezone.now() + timedelta(days=5)) &
                            Q(deadline__gte=timezone.now()),
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                )
            )
            return queryset

        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve data') from e
