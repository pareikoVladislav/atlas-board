from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from django.db.models.query import QuerySet
from django.utils import timezone

from src.choices import Status
from src.projects.dto.task import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TasksListDTO,
    TaskDetailDTO,
    TaskAnalyticsPerProjectDTO,
    TaskAnalyticsPerDeveloperDTO
)
from src.projects.repositories import TaskRepository
from src.users.models import User
from src.projects.services.service_responce import ServiceResponse
from src.shared.exception_handlers import handle_service_error


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

        except Exception as e:
            return handle_service_error(e)

    def get_task_by_id(self, task_id: int) -> ServiceResponse:
        try:
            task = self.repository.get_by_id(
                id_=task_id
            )
            response = TaskDetailDTO(instance=task)

        except Exception as e:
            return handle_service_error(e)

    def create_task(self, task_data: dict) -> ServiceResponse:
        try:
            serializer = TaskCreateDTO(data=task_data)
            serializer.is_valid(raise_exception=True)

            task = self.repository.create(**serializer.validated_data)
            return ServiceResponse(success=True, data={"id": task.id})

        except Exception as e:
            return handle_service_error(e)

    def update_task(self, task_id: int, task_data: dict, partial=False) -> ServiceResponse:
        try:
            serializer = TaskUpdateDTO(data=task_data, partial=partial)
            serializer.is_valid(raise_exception=True)

            task = self.repository.update(task_id, **serializer.validated_data)

            return ServiceResponse(success=True, data={"id": task.id})

        except Exception as e:
            return handle_service_error(e)

    def delete_task(self, task_id: int) -> ServiceResponse:
        try:
            self.repository.delete(task_id)
            return ServiceResponse(success=True, message="Task deleted")

        except Exception as e:
            return handle_service_error(e)

    def get_tasks_analytics_per_project(self):
        try:
            queryset = self.repository.get_tasks_analytics_per_project()
            serializer = TaskAnalyticsPerProjectDTO(queryset, many=True)

            return ServiceResponse(data=serializer.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def get_tasks_analytics_per_developer(self):
        try:
            queryset = self.repository.get_tasks_analytics_per_project()
            serializer = TaskAnalyticsPerDeveloperDTO(queryset, many=True)

            return ServiceResponse(data=serializer.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def assign_to_user(self, task_id: int, user: User) -> ServiceResponse:
        task_data = {"assignee": user.id}
        result = self.update_task(
                         task_id=task_id,
                         task_data=task_data,
                         partial=True)
        return result
    def complete_task(self, task_id: int):
        try:
            task_data = {"status": Status.done, "completed_at": timezone.now()}
            updated_task = self.repository.update(task_id, **task_data)
            serializer = TaskDetailDTO(instance=updated_task)
            return ServiceResponse(data=serializer.data, success=True)

        except Exception as e:
            return handle_service_error(e)