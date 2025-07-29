from datetime import timedelta
from typing import Any

from django.db.models import Count, Case, When, IntegerField, Q
from django.utils import timezone
from django.db.models.query import QuerySet
from django.db import DatabaseError, OperationalError


from src.choices import Status
from src.projects.models import Task, TaskComment
from src.projects.repositories.base import BaseRepository
from django.core.exceptions import ObjectDoesNotExist


class TaskRepository(BaseRepository):
    def __init__(self):
        super().__init__(Task)

    def get_all(self) -> QuerySet:
        """
        Получить все задачи с предзагрузкой связанных данных
        """
        try:
            qs = self.model.objects.select_related(
                'project',
                'assignee',
                'created_by'
            ).prefetch_related(
                'tags'
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

class TaskCommentRepository(BaseRepository):
    def __init__(self):
        super().__init__(TaskComment)

    def get_comments_by_task(self, task_id: int) -> QuerySet:
        """
        Получить все комментарии задачи с предзагрузкой автора
        """
        try:
            return self.model.objects.filter(
                task_id=task_id,
                deleted=False
            ).select_related('author').order_by('-created_at')
        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve comments for task {task_id}') from e
    def get_comment_by_id(self, comment_id: int) -> TaskComment:
        """
        Получить комментарий по id
        """
        try:
            return self.model.objects.get(
                id=comment_id,
                deleted=False
            )
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist(f"Comment with id {comment_id} not found")
        except DatabaseError as e:
            raise OperationalError(f'Failed to retrieve comment {comment_id}') from e

    def update_comment(self, comment_id: int, user_id: int, **update_data) -> TaskComment:
        """
        Обновить комментарий (только автор может редактировать)
        """
        try:
            comment = self.model.objects.get(
                id=comment_id,
                author_id=user_id,
                deleted=False
            )
            for field, value in update_data.items():
                setattr(comment, field, value)
            comment.save()
            return comment
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist("Comment not found or access denied")
        except DatabaseError as e:
            raise OperationalError(f'Failed to update comment {comment_id}') from e

    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        """
        Удалить комментарий (только автор может удалить)
        """
        try:
            comment = self.model.objects.get(
                id=comment_id,
                author_id=user_id,
                deleted=False
            )
            comment.deleted = True
            comment.save()
            return True
        except self.model.DoesNotExist:
            return False
        except DatabaseError as e:
            raise OperationalError(f'Failed to delete comment {comment_id}') from e

