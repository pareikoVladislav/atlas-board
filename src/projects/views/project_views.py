from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from src.projects.services.project_service import ProjectService


@api_view(['GET'])
def get_all_projects(request):
    service_response = ProjectService.get_all_projects()

    if service_response.error:
        return Response({'error': service_response.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(service_response.data, status=status.HTTP_200_OK)