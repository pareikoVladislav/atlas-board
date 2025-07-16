from typing import Any
from src.projects.repositories import ProjectRepository
from src.projects.serializers.project_dto import ProjectsListDTO
from rest_framework.response import Response
from rest_framework import status
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
            return ServiceResponse(error_type=ErrorType.UNKNOWN_ERROR,
                                   success=False,
                                   message='ошибка при получении списка проектов')