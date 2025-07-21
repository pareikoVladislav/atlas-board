from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.projects.services.project_file import ProjectFileService
from src.projects.services.service_responce import ErrorType
@api_view(['GET'])
def file_detail(request: Request, file_id: int) -> Response:
    service = ProjectFileService()
    result = service.get_project_file_by_id(file_id=file_id)
    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)
    elif result.success==False and result.error_type==ErrorType.NOT_FOUND.value:
        return Response(
            {"error": result.errors, "message": result.message},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(
        {"error": result.errors, "message": result.message},
        status=status.HTTP_400_BAD_REQUEST
    )