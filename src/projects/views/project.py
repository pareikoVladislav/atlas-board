from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.projects.services.project import ProjectService


@api_view(['GET'])
def get_all_projects(request:Request) -> Response:
    service_response = ProjectService()
    result = service_response.get_all_projects()

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['POST'])
def create_new_project(request: Request) -> Response:
    raw_data = request.data
    project_service = ProjectService()
    result = project_service.create_project(raw_data)

    if result.success:
        return Response(
            data=result.data,
            status=status.HTTP_201_CREATED
        )
    else:
        if result.error_type == 'validation_error':
            return Response(
                data={
                    'error': result.message,
                    'errors': result.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif result.error_type == 'integrity_error':
            return Response(
                data={
                    'error': result.message,
                    'errors': result.errors
                },
                status=status.HTTP_409_CONFLICT
            )
        else:
            return Response(
                data={
                    'error': result.message,
                    'errors': result.errors
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['PUT', 'PATCH'])
def update_project(request: Request, project_id: int) -> Response:
    project_data = request.data
    service = ProjectService()
    partial = True if request.method == 'PATCH' else False

    result = service.update_project(
        project_id=project_id,
        project_data=project_data,
        partial=partial
    )

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {"error": result.errors, "message": result.error_message},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def get_all_project_files(request:Request) -> Response:
    service_response = ProjectService()
    result = service_response.get_all_files()

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'message': result.message, 'errors': result.errors},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
