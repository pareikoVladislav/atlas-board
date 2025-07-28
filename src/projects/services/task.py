from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from django.db.models.query import QuerySet


from src.projects.dto.task import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TasksListDTO,
    TaskDetailDTO,
    TaskAnalyticsPerProjectDTO,
    TaskAnalyticsPerDeveloperDTO, TaskCommentListDTO, TaskCommentCreateDTO, TaskCommentUpdateDTO, TaskCommentDetailDTO
)
from src.projects.repositories import TaskRepository
from src.projects.repositories.task import TaskCommentRepository
from src.projects.services.service_responce import ServiceResponse, ErrorType


class TaskService:
    def __init__(self):
        self.repository = TaskRepository()
        self.paginator = PageNumberPagination()
        self.paginator.page_size = 10
        self.paginator.page_size_query_param = 'page_size'

    def get_page(self, request: Request, queryset: QuerySet) -> int:
        from math import ceil

        page = request.query_params.get('page')
        total_items = len(queryset)
        last_page = ceil(total_items / self.paginator.page_size)

        if page and page.isdigit() and 1 <= int(page) <= last_page:
            return int(page)

        return 1

    def get_page_size(self, request: Request) -> int:
        page_size = request.query_params.get('page_size')

        if page_size and page_size.isdigit() and 1 <= int(page_size) <= 100:
            return int(page_size)

        return self.paginator.page_size

    def get_all_tasks_paginated(self, request: Request) -> ServiceResponse:
        try:
            page_size = self.get_page_size(request)
            self.paginator.page_size = page_size

            queryset = self.repository.get_all()

            self.paginator.page = self.get_page(request, queryset)

            paginated_queryset = self.paginator.paginate_queryset(queryset, request)
            serializer = TasksListDTO(paginated_queryset, many=True)
            paginated_data = self.paginator.get_paginated_response(serializer.data).data
            return ServiceResponse(data=paginated_data, success=True)

        except Exception:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message='Error getting list of tasks'
            )

    def get_task_by_id(self, task_id: int) -> ServiceResponse:
        try:
            task = self.repository.get_by_id(
                id_=task_id
            )
            response = TaskDetailDTO(instance=task)

            return ServiceResponse(
                success=True,
                data=response.data
            )
        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND.value,
                message=str(e)
            )
        except IntegrityError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.INTEGRITY_ERROR.value,
                message=str(e)
            )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR.value,
                message=str(e)
            )

    def create_task(self, task_data: dict) -> ServiceResponse:
        serializer = TaskCreateDTO(data=task_data)
        if not serializer.is_valid():
            return ServiceResponse(
                success=False,
                errors=serializer.errors,
                error_type=ErrorType.VALIDATION_ERROR,
                message="Invalid data"
            )
        try:
            task = self.repository.create(**serializer.validated_data)
            return ServiceResponse(success=True, data={"id": task.id})
        except IntegrityError as e:
            return ServiceResponse(success=False, error_type=ErrorType.INTEGRITY_ERROR, message=str(e))
        except DatabaseError as e:
            return ServiceResponse(success=False, error_type=ErrorType.UNKNOWN_ERROR, message=str(e))

    def update_task(self, task_id: int, task_data: dict, partial=False) -> ServiceResponse:
        serializer = TaskUpdateDTO(data=task_data, partial=partial)
        if not serializer.is_valid():
            return ServiceResponse(
                success=False,
                errors=serializer.errors,
                error_type=ErrorType.VALIDATION_ERROR,
                message="Invalid data"
            )
        try:
            task = self.repository.update(task_id, **serializer.validated_data)
            return ServiceResponse(success=True, data={"id": task.id})
        except ObjectDoesNotExist as e:
            return ServiceResponse(success=False, error_type=ErrorType.NOT_FOUND, message=str(e))
        except IntegrityError as e:
            return ServiceResponse(success=False, error_type=ErrorType.INTEGRITY_ERROR, message=str(e))
        except DatabaseError as e:
            return ServiceResponse(success=False, error_type=ErrorType.UNKNOWN_ERROR, message=str(e))

    def delete_task(self, task_id: int) -> ServiceResponse:
        try:
            self.repository.delete(task_id)
            return ServiceResponse(success=True, message="Task deleted")
        except ObjectDoesNotExist as e:
            return ServiceResponse(success=False, error_type=ErrorType.NOT_FOUND, message=str(e))
        except DatabaseError as e:
            return ServiceResponse(success=False, error_type=ErrorType.UNKNOWN_ERROR, message=str(e))

    def get_tasks_analytics_per_project(self):
        try:
            queryset = self.repository.get_tasks_analytics_per_project()
            serializer = TaskAnalyticsPerProjectDTO(queryset, many=True)
            return ServiceResponse(data=serializer.data, success=True)

        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR,
                message=str(e)
            )

        except Exception as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message=str(e)
            )

    def get_tasks_analytics_per_developer(self):
        try:
            queryset = self.repository.get_tasks_analytics_per_project()
            serializer = TaskAnalyticsPerDeveloperDTO(queryset, many=True)
            return ServiceResponse(data=serializer.data, success=True)

        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR,
                message=str(e)
            )

        except Exception as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message=str(e)
            )


class TaskCommentService:
    def __init__(self):
        self.repository = TaskCommentRepository()

    def create_comment(self, request: Request, task_id: int) -> ServiceResponse:
        """Создать комментарий к задаче"""
        serializer = TaskCommentCreateDTO(
            data=request.data,
            context={'request': request, 'view': type('MockView', (), {'kwargs': {'task_id': task_id}})()}
        )

        if not serializer.is_valid():
            return ServiceResponse(
                success=False,
                errors=serializer.errors,
                error_type=ErrorType.VALIDATION_ERROR,
                message="Invalid data"
            )

        try:
            comment = serializer.save()
            response_data = TaskCommentListDTO(comment).data
            return ServiceResponse(success=True, data=response_data)
        except IntegrityError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.INTEGRITY_ERROR,
                message=str(e)
            )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR,
                message=str(e)
            )

    def get_task_comments(self, task_id: int) -> ServiceResponse:
        """Получить все комментарии задачи"""
        try:
            comments = self.repository.get_comments_by_task(task_id)
            serializer = TaskCommentListDTO(comments, many=True)
            return ServiceResponse(success=True, data=serializer.data)
        except Exception as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message=f'Error getting comments: {str(e)}'
            )

    def get_comment(self, comment_id: int):
        """Получить комментарий по id"""
        try:
            comment = self.repository.get_comment_by_id(comment_id)
            response_data = TaskCommentListDTO(comment).data
            return ServiceResponse(success=True, data=response_data)
        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND,
                message=str(e)
            )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR,
            )


    def update_comment(self, comment_id: int, request: Request) -> ServiceResponse:
        """Обновить комментарий"""
        serializer = TaskCommentUpdateDTO(data=request.data)

        if not serializer.is_valid():
            return ServiceResponse(
                success=False,
                errors=serializer.errors,
                error_type=ErrorType.VALIDATION_ERROR,
                message="Invalid data"
            )

        try:
            comment = self.repository.update_comment(
                comment_id,
                request.user.id,
                **serializer.validated_data
            )
            response_data = TaskCommentListDTO(comment).data
            return ServiceResponse(success=True, data=response_data)
        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND,
                message=str(e)
            )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR,
                message=str(e)
            )

    def delete_comment(self, comment_id: int, user_id: int) -> ServiceResponse:
        """Удалить комментарий"""
        try:
            success = self.repository.delete_comment(comment_id, user_id)
            if success:
                return ServiceResponse(success=True, message="Comment deleted")
            else:
                return ServiceResponse(
                    success=False,
                    error_type=ErrorType.NOT_FOUND,
                    message="Comment not found or access denied"
                )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR,
                message=str(e)
            )
