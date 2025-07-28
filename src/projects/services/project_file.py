from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError
from rest_framework.request import Request


from src.projects.models import ProjectFile, Project
from src.projects.repositories import ProjectFileRepository
from src.projects.services.service_responce import ServiceResponse, ErrorType
from src.projects.services.project import ProjectService
from src.projects.dto import ProjectFileDetailDTO, CreateProjectFileDTO


class ProjectFileService:
    def __init__(self):
        self.repository = ProjectFileRepository()

    def create(self, request: Request) -> ServiceResponse:
        """Get request data, prepare data for serializing.
        Call CreateProjectFileDTO, validate data, create file object by project.
        Prepare ServiceResponse."""

        try:
            project = request.data.get('project_id')
            file = request.FILES.get('file')
            user = request.user
            project_service = ProjectService()
            project_obj = project_service.get_project_by_id(int(project)).data
            serializer = CreateProjectFileDTO(
                data={
                    "name": file.name,
                    "file": file
                },
                context={
                    "project": project_obj,
                    "user": user,
                }
            )
            if not serializer.is_valid():
                return ServiceResponse(
                    success=False,
                    error_type=ErrorType.VALIDATION_ERROR,
                    errors=serializer.errors,
                )
            serializer.save()
            return ServiceResponse(
                success=True,
                data=serializer.data,
            )
        except Exception as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR,
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
                error_type=ErrorType.NOT_FOUND,
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