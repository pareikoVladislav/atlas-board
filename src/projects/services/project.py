from src.projects.dto.filters import ProjectFilterDTO
from src.projects.repositories.project import ProjectRepository
from src.projects.dto import (
    ProjectUpdateDTO,
    ProjectCreateDTO,
    ProjectDetailDTO,
    ProjectsListDTO,
    ProjectFileDTO,
)
from src.projects.services.service_responce import ServiceResponse
from src.shared.exception_handlers import handle_service_error


class ProjectService:
    def __init__(self):
        self.repository = ProjectRepository()

    def get_all_projects(self) -> ServiceResponse:
        try:
            projects = self.repository.get_all()
            serializer = ProjectsListDTO(projects, many=True)

            return ServiceResponse(data=serializer.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def create_project(self, project_data: dict) -> ServiceResponse:
        try:
            serializer = ProjectCreateDTO(data=project_data)
            serializer.is_valid(raise_exception=True)

            project = self.repository.create(**serializer.validated_data)
            response = ProjectDetailDTO(project)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def update_project(
            self,
            project_id: int,
            project_data: dict,
            partial=False
    ) -> ServiceResponse:
        try:
            serializer = ProjectUpdateDTO(data=project_data, partial=partial)
            serializer.is_valid(raise_exception=True)

            updated_project = self.repository.update(
                id_=project_id,
                **serializer.validated_data
            )
            response = ProjectDetailDTO(updated_project)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def get_all_projects_filtered(self, query_params: dict) -> ServiceResponse:
        try:
            serializer = ProjectFilterDTO(data=query_params)
            serializer.is_valid(raise_exception=True)

            filters = serializer.validated_data
            ordering = filters.pop('ordering', None)

            projects = self.repository.get_filtered_projects(
                filters=filters,
                ordering=ordering
            )
            response = ProjectsListDTO(projects, many=True)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def get_all_files(self, project_id: int) -> ServiceResponse:
        try:
            files = self.repository.get_all_project_files(project_id)
            response = ProjectFileDTO(files, many=True)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def get_project_by_id(self, project_id: int) -> ServiceResponse:
        try:
            project = self.repository.get_by_id(id_=project_id)
            response = ProjectDetailDTO(instance=project)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)
