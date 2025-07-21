from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.users.services import UserService


@api_view(['GET'])
def get_all_users(request:Request) -> Response:

    project_name = request.query_params.get('project_name')
    tasks_from = request.query_params.get('tasks_from')
    tasks_to = request.query_params.get('tasks_to')

    try:
        tasks_from = int(tasks_from) if tasks_from is not None else None
        tasks_to = int(tasks_to) if tasks_to is not None else None
    except ValueError:
        return Response(
            {'message': 'tasks_from and tasks_to must be integers'},
            status=status.HTTP_400_BAD_REQUEST
        )

    service_response = UserService()
    result = service_response.get_all_users(
        project_name=project_name,
        tasks_from=tasks_from,
        tasks_to=tasks_to
    )

    if result.success:
        return Response(data = result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

@api_view(['GET'])
def retrieve_user(request:Request, user_id: int) -> Response:
    service_response = UserService()
    result = service_response.retrieve_user(user_id)

    if result.success:
        return Response(data = result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )