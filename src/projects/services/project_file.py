from rest_framework.request import Request

from src.projects.repositories import ProjectFileRepository
from src.projects.services.service_responce import ServiceResponse
from src.projects.services.project import ProjectService
from src.projects.dto import ProjectFileDetailDTO, CreateProjectFileDTO
from src.shared.exception_handlers import handle_service_error


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
                data={"name": file.name,"file": file},
                context={"project": project_obj, "user": user}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return ServiceResponse(success=True, data=serializer.data)

        except Exception as e:
            return handle_service_error(e)

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

        except Exception as e:
            return handle_service_error(e)