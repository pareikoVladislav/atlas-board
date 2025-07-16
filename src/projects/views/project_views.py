from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.projects.services.project_service import ProjectService


@api_view(['GET'])
def get_all_projects(request:Request) -> Response:
    service_response = ProjectService()
    result = service_response.get_all_projects()

    if result.success:
        return Response(data = result.data, status=status.HTTP_200_OK)

    return Response({'message': result.message,'errors': result.errors},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)