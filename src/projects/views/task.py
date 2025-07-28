from rest_framework.viewsets import ModelViewSet

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from src.projects.services.task import TaskService
from src.projects.models import Task
from src.projects.dto.task import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TasksListDTO,
    TaskDetailDTO
)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    service = TaskService()

    # def get_queryset(self):
    #     return self.service.repository.get_all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TasksListDTO
        elif self.action == 'retrieve':
            return TaskDetailDTO
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateDTO
        return TaskCreateDTO

    @action(methods=["get"], detail=False, url_path="analytics-per-project")
    def analytics_per_project(self, request: Request) -> Response:

        result = self.service.get_tasks_analytics_per_project()

        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)

        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


    @action(methods=["get"], detail=False, url_path="analytics-per-developer")
    def analytics_per_developer(self, request: Request) -> Response:

        result = self.service.get_tasks_analytics_per_developer()

        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)

        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(methods=["post"], detail=True, url_path="assign-to-me")
    def assign_to_me(self, request: Request, task_id: int) -> Response:
        result = self.service.assign_to_user(task_id, request.user)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)