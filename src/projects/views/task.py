from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.projects.services.task import TaskServise



@api_view(['GET'])
def get_all_tasks(requests) -> Response:
    service_response = TaskServise()
    result = service_response.get_all_tasks()

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['GET'])
def get_task_by_id(requests, task_id: int) -> Response:
    service_response = TaskServise()
    result = service_response.get_task_by_id(task_id=task_id)
    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {"error": result.errors, "message": result.message},
        status=status.HTTP_400_BAD_REQUEST
    )

