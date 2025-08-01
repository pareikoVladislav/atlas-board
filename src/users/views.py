from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend

from src.users.filters import UserFilter
from src.users.services import UserService

class UserListGenericView(GenericAPIView):
    service = UserService()
    queryset = service.repository.get_all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get(self, request: Request) -> Response:
        result = self.service.get_all_users(
            filters=request.query_params
        )

        if result.success:
            return Response(data=result.data, status=status.HTTP_200_OK)

        return Response(
            {'message': result.message, 'errors': result.errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def retrieve_user(request: Request, user_id: int) -> Response:
    service_response = UserService()
    result = service_response.retrieve_user(user_id)

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
