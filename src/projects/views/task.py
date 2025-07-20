from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.projects.services.task import TaskService


@api_view(['GET', 'POST'])
def task_list(request: Request) -> Response:
    service = TaskService()

    if request.method == 'GET':
        result = service.get_all_tasks()
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
