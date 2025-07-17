from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.users.services import UserService


@api_view(['GET'])
def get_all_users(request:Request) -> Response:
    service_response = UserService()
    result = service_response.get_all_users()

    if result.success:
        return Response(data = result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

@api_view(['GET'])
def get_by_id(request:Request) -> Response:
    service_response = UserService()
    result = service_response.get_by_id()

    if result.success:
        return Response(data = result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )