from typing import Any
from src.projects.repositories import ProjectRepository
from src.projects.serializers.project_dto import ProjectsListDTO
from rest_framework.response import Response
from rest_framework import status


class ErrorType:
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'


class ServiceResponse:
    def __init__(self, data: Any = None, error: str = ''):
        self.data = data
        self.error = error


class ProjectService:
    @staticmethod
    def get_all_projects() -> ServiceResponse:
        try:
            repository = ProjectRepository()
            projects = repository.get_all()
            serializer = ProjectsListDTO(projects, many=True)
            return ServiceResponse(data=serializer.data)
        except Exception:
            return ServiceResponse(error=ErrorType.UNKNOWN_ERROR)