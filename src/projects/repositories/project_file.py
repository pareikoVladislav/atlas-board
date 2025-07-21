from typing import TypeVar
from django.db.models import Model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import DatabaseError, OperationalError, IntegrityError, transaction


from src.projects.repositories import BaseRepository
from src.projects.models import ProjectFile


Model_ = TypeVar('Model_', bound=Model)

class ProjectFileRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProjectFile)







