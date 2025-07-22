from django.db import IntegrityError, DatabaseError
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from src.users.repositories import UserRepository
from src.users.dto import UserDetailDTO, UsersListDTO
from src.projects.services.service_responce import ServiceResponse, ErrorType


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self) -> ServiceResponse:
        try:
            projects = self.repository.get_all()
            serializer = UsersListDTO(projects, many=True)
            return ServiceResponse(data=serializer.data, success=True)
        except Exception:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message='Error getting list of projects'
            )

    def retrieve_user(self, user_id: int) -> ServiceResponse:
        try:
            user = self.repository.get_by_id(
                id_=user_id
            )
            response = UserDetailDTO(instance=user)

            return ServiceResponse(
                success=True,
                data=response.data
            )
        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND.value,
                message=str(e)
            )
        except IntegrityError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.INTEGRITY_ERROR.value,
                message=str(e)
            )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR.value,
                message=str(e)
            )

    def retrieve_user_by_email(self, user_email: str) -> ServiceResponse:
        try:
            user = self.repository.get_by_email(
                email=user_email
            )
            response = UserDetailDTO(instance=user)

            return ServiceResponse(
                success=True,
                data=response.data
            )
        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND.value,
                message=str(e)
            )
        except IntegrityError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.INTEGRITY_ERROR.value,
                message=str(e)
            )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR.value,
                message=str(e)
            )