from django.db import IntegrityError, DatabaseError
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from src.projects.repositories.project import ProjectRepository
from src.projects.dto import ProjectUpdateDTO, ProjectCreateDTO, ProjectDetailDTO, ProjectsListDTO
from src.projects.services.service_responce import ServiceResponse, ErrorType


class ProjectService:
    def __init__(self):
        self.repository = ProjectRepository()

    def get_all_projects(self) -> ServiceResponse:
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

    def create_project(self, project_data: dict) -> ServiceResponse:
        try:
            serializer = ProjectCreateDTO(data=project_data)
            serializer.is_valid(raise_exception=True)

            project = self.repository.create(**serializer.data)
            serialized_response = ProjectDetailDTO(project)
            return ServiceResponse(
                data=serialized_response.data,
                success=True
            )

        except ValidationError as e:
            return ServiceResponse(
                error_type=ErrorType.VALIDATION_ERROR,
                success=False,
                message="Invalid data",
                errors=serializer.errors
            )

        except IntegrityError as e:
            return ServiceResponse(
                error_type=ErrorType.INTEGRITY_ERROR,
                success=False,
                message=str(e)
            )

        except DatabaseError as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message=str(e)
            )

        except Exception as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message=f'Failed to create object {e}'
            )

    def update_project(self, project_id: int, project_data: dict, partial=False):
        try:
            update_serializer = ProjectUpdateDTO(
                data=project_data,
                partial=partial)
            if not update_serializer.is_valid():
                return ServiceResponse(
                    errors=update_serializer.errors,
                    error_type=ErrorType.VALIDATION_ERROR.value,
                    success=False)
            updated_project = self.repository.update(
                id_=project_id,
                **update_serializer.validated_data)
            response = ProjectDetailDTO(updated_project)
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
