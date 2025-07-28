from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.projects.services.time_entry import TimeEntryService


@api_view(['POST'])
def create_time_entry(request: Request) -> Response:
    service = TimeEntryService()
    current_user = request.user
    time_entry_data = request.data

    time_entry_data['user'] = current_user['username']
    result = service.create_time_entry(time_entry_data)

    if result.success:
        return Response(result.to_dict(), status=status.HTTP_201_CREATED)

    return Response(result.to_dict(), status=status.HTTP_400_BAD_REQUEST)
