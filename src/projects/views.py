from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from src.projects.services import ProjectService

@api_view(['PUT', 'PATCH'])
def update_project(request: Request, project_id: int) -> Response:
    project_data = request.data
    servise = ProjectService()
    result = servise.update_project(
        project_id=project_id,
        project_data=project_data
    )

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response({"error": result.errors, "message": result.error_message}, status=status.HTTP_400_BAD_REQUEST)


    return Response(
        data=result,
        status=status.HTTP_200_OK
    )

