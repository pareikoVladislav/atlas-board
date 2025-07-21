from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError

from src.projects.repositories import ProjectRepository
from src.projects.services.service_responce import ServiceResponse, ErrorType
from src.projects.dto import ProjectFileDetailDTO


class ProjectFileService:
    def __init__(self):
        self.repository = ProjectRepository()

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