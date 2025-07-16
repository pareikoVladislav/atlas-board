from src.projects.models.project import Project
# from src.projects.repositories.base import BaseRepository  # пока не реализован

class BaseRepository:
    pass


class ProjectRepository(BaseRepository):
    def __init__(self):
        self.model = Project

    def get_all(self):
        return self.model.objects.all()