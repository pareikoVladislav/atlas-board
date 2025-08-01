from typing import Any

from django.db import IntegrityError, DatabaseError
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from src.shared.exception_handlers import handle_service_error
from src.users.filters import UserFilter
from src.users.repositories import UserRepository
from src.users.dto import UserDetailDTO, UsersListDTO
from src.projects.services.service_responce import ServiceResponse, ErrorType


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self, filters: dict[str, Any] = None) -> ServiceResponse:
        try:
            users_qs = self.repository.get_all()
            if filters:
                users_qs = UserFilter(filters, users_qs).qs
            response = UsersListDTO(users_qs, many=True)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def retrieve_user(self, user_id: int) -> ServiceResponse:
        try:
            user = self.repository.get_by_id(id_=user_id)
            response = UserDetailDTO(instance=user)

            return ServiceResponse(success=True, data=response.data)

        except Exception as e:
            return handle_service_error(e)
