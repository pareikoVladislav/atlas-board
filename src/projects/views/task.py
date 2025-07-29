from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import AnonymousUser

from src.projects.services.service_responce import ErrorType
from src.projects.services.task import TaskService, TaskCommentService
from rest_framework.views import APIView


class TaskCommentsAPIView(APIView):
    service = TaskCommentService()

    def get(self, request: Request, task_id: int) -> Response:
        """
        GET: Получить все комментарии задачи
        """

        result = self.service.get_task_comments(task_id)
        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)
        return Response(
            {'message': result.message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def post(self, request: Request, task_id: int) -> Response:
        """
        POST: Создать новый комментарий
        """
        result = self.service.create_comment(request, task_id)
        if result.success:
            return Response(result.data, status=status.HTTP_201_CREATED)
        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class TaskCommentDetailAPIView(APIView):
    service = TaskCommentService()

    def get(self, request: Request, task_id: int, comment_id: int) -> Response:
        """
        GET: получить конкретный комментарий по id
        """
        result = self.service.get_comment(comment_id)
        if result.success:
            return Response(result.data, status=status.HTTP_200_OK)

    def put(self, request: Request, task_id: int, comment_id: int) -> Response:
        """
        PUT: Редактировать комментарий
        """
        result = self.service.update_comment(comment_id, request)
        if result.success:
            return Response(result.data, status=status.HTTP_200_OK)

        error_status = status.HTTP_404_NOT_FOUND if result.error_type == ErrorType.NOT_FOUND else status.HTTP_400_BAD_REQUEST
        return Response(
            {'message': result.message, 'errors': result.errors},
            status=error_status
        )

    def delete(self, request: Request, task_id: int, comment_id: int) -> Response:
        result = self.service.delete_comment(comment_id, request.user.id)
        if result.success:
            return Response({'message': result.message}, status=status.HTTP_200_OK)

        error_status = status.HTTP_404_NOT_FOUND if result.error_type == ErrorType.NOT_FOUND else status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response({'message': result.message}, status=error_status)
from src.projects.services.task import TaskService
from src.projects.services.service_responce import ErrorType
from src.users.models import User


class TaskViewSet(ViewSet):
    lookup_url_kwarg = 'task_id'
    lookup_fields = 'task_id'
    service = TaskService()

    def list(self, request: Request) -> Response:
        result = self.service.get_all_tasks_paginated(request)
        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)
        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def retrieve(self, request: Request, task_id: int) -> Response:
        result = self.service.get_task_by_id(task_id=task_id)
        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)
        if result.error_type==ErrorType.NOT_FOUND:
            return Response(
                {'message': result.message, 'errors': result.errors},status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"error": result.errors, "message": result.message},
            status=status.HTTP_400_BAD_REQUEST
        )

    def create(self, request) -> Response:
        result = self.service.create_task(request.data)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_201_CREATED)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, task_id: int) -> Response:
        result = self.service.update_task(task_id, request.data, partial=False)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, task_id: int) -> Response:
        result = self.service.update_task(task_id, request.data, partial=True)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, task_id: int) -> Response:
        result = self.service.delete_task(task_id)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def assign_to_me(self, request: Request, task_id: int) -> Response:
        #TODO вернутся после реализации аутентификации и удалить костыль
        user = request.user
        if isinstance(user, AnonymousUser):
            user = User.objects.filter(is_superuser=True).first()
        result = self.service.assign_to_user(task_id, user)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def analytics_per_project(self, request: Request) -> Response:
        service = TaskService()
        result = service.get_tasks_analytics_per_project()

        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)

        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=False, methods=["get"])
    def analytics_per_developer(self, request: Request) -> Response:
        service = TaskService()
        result = service.get_tasks_analytics_per_developer()

        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)

        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )





