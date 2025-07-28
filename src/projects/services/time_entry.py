from rest_framework.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError

from src.projects.dto import TimeEntryCreateDTO, TimeEntryDTO
from src.projects.repositories.time_entry import TimeEntryRepository
from src.projects.services.service_responce import ServiceResponse
from src.shared.exception_handlers import (
    handle_validation_error,
    handle_integrity_error,
    handle_database_error,
    handle_unknown_error
)


class TimeEntryService:
    def __init__(self):
        self.repository = TimeEntryRepository()

    def create_time_entry(self, data: dict) -> ServiceResponse:
        try:
            serializer = TimeEntryCreateDTO(data=data)
            serializer.is_valid(raise_exception=True)

            time_entry = self.repository.create(**serializer.validated_data)
            result = TimeEntryDTO(data=time_entry).data
            return ServiceResponse(success=True, data=result)

        except ValidationError as e:
            return handle_validation_error(e, serializer)
        except IntegrityError as e:
            return handle_integrity_error(e)
        except DatabaseError as e:
            return handle_database_error(e)
        except Exception as e:
            return handle_unknown_error(e)
