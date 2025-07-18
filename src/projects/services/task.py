from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError
from src.projects.repositories import TaskRepository
from src.projects.services.service_responce import (
    ServiceResponse,
    ErrorType,
)
from src.projects.dto import TasksListDTO, TaskDetailDTO

class TaskServise:
    def __init__(self):
        self.repository = TaskRepository()

    def get_all_tasks(self) -> ServiceResponse:
        try:
            tasks = self.repository.get_all()
            serializer = TasksListDTO(tasks, many=True)
            return ServiceResponse(data=serializer.data, success=True)
        except Exception:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR,
                success=False,
                message='Error getting list of tasks'
            )

    def get_task_by_id(self, task_id: int) -> ServiceResponse:
        try:
            task = self.repository.get_by_id(
                id_=task_id
            )
            response = TaskDetailDTO(instance=task)

            return ServiceResponse(
                success=True,
                data=response.data
            )
        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND.value,
                message=str(e)
            )
        except IntegrityError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.INTEGRITY_ERROR.value,
                message=str(e)
            )
        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR.value,
                message=str(e)
            )
