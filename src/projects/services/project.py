from src.projects.repositories.project import  ProjectRepository
from src.projects.dto import ProjectUpdateDTO, ProjectDetailDTO

class ProjectService:
    def __init__(self):
        self.repository = ProjectRepository()

    def update_project(self, project_id: int, project_data: dict):
        update_serializer = ProjectUpdateDTO(project_data)
        if not update_serializer.is_valid():
            updated_project = self.repository.update_by_id(project_id=project_id, **update_serializer.validated_data)
            response=ProjectDetailDTO(updated_project)
            return response
        return update_serializer.errors
