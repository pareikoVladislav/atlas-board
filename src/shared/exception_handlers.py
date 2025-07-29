from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, DatabaseError

from src.projects.services.service_responce import ErrorType, ServiceResponse


def handle_service_error(err: Exception, serializer=None) -> ServiceResponse:
    error_mapping = {
        ObjectDoesNotExist: ErrorType.NOT_FOUND,
        ValidationError: ErrorType.VALIDATION_ERROR,
        IntegrityError: ErrorType.INTEGRITY_ERROR,
        DatabaseError: ErrorType.UNKNOWN_ERROR
    }

    matched_type = error_mapping.get(type(err), ErrorType.UNKNOWN_ERROR)

    return ServiceResponse(
        success=False,
        error_type=matched_type,
        message=str(err),
        errors=serializer.errors if serializer else None
    )
