from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError

from src.projects.models import ProjectFile, Project
from src.projects.repositories import ProjectRepository
from src.projects.services.service_responce import ServiceResponse, ErrorType
from src.projects.dto import ProjectFileDetailDTO, CreateProjectFileDTO
from src.users.models import User


class ProjectFileService:
    def __init__(self):
        self.repository = ProjectRepository()

    def create(self, data: dict, project: Project, user: User, file: bytes):
        try:
            data.update({"file": file})
            print("wir sind da")
            serializer = CreateProjectFileDTO(
                data=data,
                context={
                    "project": project,
                    "user": user,
            }
            )
            print("not valid")
            if not serializer.is_valid():
                print("not valid")
                return ServiceResponse(
                    success=False,
                    error_type=ErrorType.VALIDATION_ERROR.value,
                    errors=serializer.errors,
                )
            print("wir go save serializer")
            serializer.save()
            return ServiceResponse(
                success=True,
                data=serializer.data,
            )
        except Exception as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR.value,
                errors=str(e),
            )

    def get_project_file_by_id(self, file_id: int) -> ServiceResponse:
        try:
            file = self.repository.get_by_id(
                id_=file_id
            )
            response = ProjectFileDetailDTO(instance=file)

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