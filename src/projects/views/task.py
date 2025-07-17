from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.projects.services.task import TaskService


@api_view(['POST'])
def create_task(request: Request) -> Response:
    service = TaskService()
    result = service.create_task(request.data)

    if result.success:
        return Response(result.to_dict(), status=status.HTTP_201_CREATED)

    return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_task(request: Request, task_id: int) -> Response:
    service = TaskService()
    partial = request.method == 'PATCH'
    result = service.update_task(task_id, request.data, partial)

    if result.success:
        return Response(result.to_dict(), status=status.HTTP_200_OK)

    return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_task(request: Request, task_id: int) -> Response:
    service = TaskService()
    result = service.delete_task(task_id)

    if result.success:
        return Response(result.to_dict(), status=status.HTTP_200_OK)

    return Response(result.to_dict(), status=status.HTTP_404_NOT_FOUND)
