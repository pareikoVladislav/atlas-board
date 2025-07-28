from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.projects.services.service_responce import ErrorType
from src.projects.services.task import TaskService, TaskCommentService
from rest_framework.views import APIView


class TaskCommentsAPIView(APIView):
    def get(self, request: Request, task_id: int) -> Response:
        """
        GET: Получить все комментарии задачи
        """
        service = TaskCommentService()

        result = service.get_task_comments(task_id)
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

        service = TaskCommentService()
        result = service.create_comment(request, task_id)
        if result.success:
            return Response(result.data, status=status.HTTP_201_CREATED)
        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class TaskCommentDetailAPIView(APIView):
    def get(self, request: Request, task_id: int, comment_id: int) -> Response:
        """
        GET: получить конкретный комментарий по id
        """
        service = TaskCommentService()

        result = service.get_comment(comment_id)
        if result.success:
            return Response(result.data, status=status.HTTP_200_OK)

    def put(self, request: Request, task_id: int, comment_id: int) -> Response:
        """
        PUT: Редактировать комментарий
        """
        service = TaskCommentService()

        result = service.update_comment(comment_id, request)
        if result.success:
            return Response(result.data, status=status.HTTP_200_OK)

        error_status = status.HTTP_404_NOT_FOUND if result.error_type == ErrorType.NOT_FOUND else status.HTTP_400_BAD_REQUEST
        return Response(
            {'message': result.message, 'errors': result.errors},
            status=error_status
        )

    def delete(self, request: Request, task_id: int, comment_id: int) -> Response:
        service = TaskCommentService()
        result = service.delete_comment(comment_id, request.user.id)
        if result.success:
            return Response({'message': result.message}, status=status.HTTP_200_OK)

        error_status = status.HTTP_404_NOT_FOUND if result.error_type == ErrorType.NOT_FOUND else status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response({'message': result.message}, status=error_status)


@api_view(['GET', 'POST'])
def task_list(request: Request) -> Response:
    service = TaskService()

    if request.method == 'GET':
        result = service.get_all_tasks_paginated(request)
        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)
        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if request.method == 'POST':
        result = service.create_task(request.data)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_201_CREATED)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def task_detail(request: Request, task_id: int) -> Response:
    service = TaskService()

    if request.method == 'GET':
        result = service.get_task_by_id(task_id=task_id)
        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)
        return Response(
            {"error": result.errors, "message": result.message},
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        result = service.update_task(task_id, request.data, partial)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)
        return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        result = service.delete_task(task_id)
        if result.success:
            return Response(result.to_dict(), status=status.HTTP_200_OK)
        return Response(result.to_dict(), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def analytics_per_project(request: Request) -> Response:
    service = TaskService()
    result = service.get_tasks_analytics_per_project()

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['GET'])
def analytics_per_developer(request: Request) -> Response:
    service = TaskService()
    result = service.get_tasks_analytics_per_developer()

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
