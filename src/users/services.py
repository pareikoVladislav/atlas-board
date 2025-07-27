from django.db import IntegrityError, DatabaseError
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from src.users.repositories import UserRepository
from src.users.dto import UserDetailDTO, UsersListDTO
from src.projects.services.service_responce import ServiceResponse, ErrorType


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self, project_name=None, tasks_from=None, tasks_to=None) -> ServiceResponse:
        try:
            users_qs = self.repository.get_all()

            if project_name:
                users_qs = users_qs.filter(main_project__name__icontains=project_name)

            if tasks_from is not None:
                users_qs = users_qs.annotate(task_count=Count('assigned_tasks')).filter(task_count__gte=tasks_from)

            if tasks_to is not None:
                users_qs = users_qs.annotate(task_count=Count('assigned_tasks')).filter(task_count__lte=tasks_to)

            serializer = UsersListDTO(users_qs, many=True)
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