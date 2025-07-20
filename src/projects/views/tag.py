from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from src.projects.services.project import ProjectService
from src.projects.services.tag import TagService


@api_view(['GET'])
def get_all_tags(request: Request) -> Response:
    tag_service = TagService()
    result = tag_service.get_all_tags()

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'error': result.message},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['POST'])
def create_tag(request: Request) -> Response:
    raw_data = request.data
    tag_service = TagService()
    result = tag_service.create_tag(raw_data)

    if result.success:
        return Response(
            data=result.data,
            status=status.HTTP_201_CREATED
        )
    else:
        if result.error_type == 'validation_error':
            return Response(
                data={'error': result.message},
                status=status.HTTP_400_BAD_REQUEST
            )

        elif result.error_type == 'integrity_error':
            return Response(
                data={'error': result.message},
                status=status.HTTP_409_CONFLICT
            )
        else:
            return Response(
                data={'error': result.message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['PUT', 'PATCH'])
def update_tag(request: Request, tag_id: int) -> Response:
    raw_data = request.data
    tag_service = TagService()

    partial = True if request.method == 'PATCH' else False

    result = tag_service.update_tag(
        tag_id=tag_id,
        tag_data=raw_data,
        partial=partial
    )

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {"error": result.message},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
def delete_tag(request: Request, tag_id: int) -> Response:
    tag_service = TagService()
    result = tag_service.delete_tag(tag_id)

    if result.success:
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        if result.error_type == 'not_found':
            return Response(
                data={'error': result.message},
                status=status.HTTP_404_NOT_FOUND
            )

        else:
            return Response(
                data={'error': result.message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
def get_tag_by_id(request: Request, tag_id: int) -> Response:
    tag_service = TagService()
    result = tag_service.get_tag_by_id(tag_id)

    if result.success:
        return Response(data=result.data, status=status.HTTP_200_OK)

    return Response(
        {'error': result.message},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
