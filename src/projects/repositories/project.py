from typing import TypeVar, Optional
from django.db.models import Model, QuerySet
from django.db import DatabaseError, OperationalError

from src.projects.models.project import Project
from src.projects.repositories.base import BaseRepository


Model_ = TypeVar('Model_', bound=Model)

class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)

    def get_all_project_files(self, id_: int) -> Optional[Model_]:
        if isinstance(id_, int) and id_ > 0:
            try:
                obj = self.model.objects.get(id=id_)
                files = obj.files.all()
                return files
            except self.model.DoesNotExist:
                return None
            except DatabaseError as e:
                raise OperationalError(f'Failed to retrieve {self.model.__name__} with id {id_}') from e
        else:
            raise ValueError('id must be positive integer')


