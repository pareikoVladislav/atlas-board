from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.projects.services.project_file import ProjectFileService

@api_view(['GET'])
def file_detail(request: Request, file_id: int) -> Response:
    service = ProjectFileService()
    result = service.get_project_file_by_id(file_id=file_id)
    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)
    return Response(
        {"error": result.errors, "message": result.message},
        status=status.HTTP_400_BAD_REQUEST
    )