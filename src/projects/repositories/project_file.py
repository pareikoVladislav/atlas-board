from src.projects.repositories import ProjectRepositoryq
from src.projects.models import ProjectFile

class ProjectFileRepository(ProjectRepositoryq):
    def __init__(self):
        super().__init__(ProjectFile)
