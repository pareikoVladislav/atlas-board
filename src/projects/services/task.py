from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError

from src.projects.dto.task import TaskCreateDTO, TaskUpdateDTO
from src.projects.models import Task
from src.projects.repositories import BaseRepository
from src.projects.services.service_responce import ServiceResponse, ErrorType


class TaskService:
    def __init__(self):
        self.repository = BaseRepository(Task)

    def create_task(self, task_data: dict) -> ServiceResponse:
        serializer = TaskCreateDTO(data=task_data)
        if not serializer.is_valid():
            return ServiceResponse(
                success=False,
                errors=serializer.errors,
                error_type=ErrorType.VALIDATION_ERROR,
                message="Invalid data"
            )
        try:
            task = self.repository.create(**serializer.validated_data)
            return ServiceResponse(success=True, data={"id": task.id})
        except IntegrityError as e:
            return ServiceResponse(success=False, error_type=ErrorType.INTEGRITY_ERROR, message=str(e))
        except DatabaseError as e:
            return ServiceResponse(success=False, error_type=ErrorType.UNKNOWN_ERROR, message=str(e))


    def update_task(self, task_id:int, task_data: dict, partial=False) -> ServiceResponse:
        serializer = TaskUpdateDTO(data=task_data, partial=partial)
        if not serializer.is_valid():
            return ServiceResponse(
                success=False,
                errors=serializer.errors,
                error_type=ErrorType.VALIDATION_ERROR,
                message="Invalid data"
            )
        try:
            task = self.repository.update(task_id, **serializer.validated_data)
            return ServiceResponse(success=True, data={"id": task.id})
        except ObjectDoesNotExist as e:
            return ServiceResponse(success=False, error_type=ErrorType.NOT_FOUND, message=str(e))
        except IntegrityError as e:
            return ServiceResponse(success=False, error_type=ErrorType.INTEGRITY_ERROR, message=str(e))
        except DatabaseError as e:
            return ServiceResponse(success=False, error_type=ErrorType.UNKNOWN_ERROR, message=str(e))


    def delete_task(self, task_id:int) -> ServiceResponse:
        try:
            self.repository.delete(task_id)
            return ServiceResponse(success=True, message="Task deleted")
        except ObjectDoesNotExist as e:
            return ServiceResponse(success=False, error_type=ErrorType.NOT_FOUND, message=str(e))
        except DatabaseError as e:
            return ServiceResponse(success=False, error_type=ErrorType.UNKNOWN_ERROR, message=str(e))
