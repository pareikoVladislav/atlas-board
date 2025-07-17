from django.db import IntegrityError, DatabaseError
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from src.users.repositories import UserRepository
from src.users.dto import ProjectDetailDTO, ProjectsListDTO
from src.projects.services.service_responce import ServiceResponse, ErrorType


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self) -> ServiceResponse:
        try:
            projects = self.repository.get_all()
            serializer = ProjectsListDTO(projects, many=True)
            return ServiceResponse(data=serializer.data, success=True)
        except Exception:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message='Error getting list of projects'
            )

    def get_by_id(self, user_id: int) -> ServiceResponse:
        pass