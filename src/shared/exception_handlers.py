from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, DatabaseError

from src.projects.services.service_responce import ErrorType, ServiceResponse


def handle_validation_error(err: ValidationError, serializer) -> ServiceResponse:
    return ServiceResponse(
        error_type=ErrorType.VALIDATION_ERROR,
        success=False,
        message=str(err),
        errors=serializer.errors
    )


def handle_integrity_error(err: IntegrityError) -> ServiceResponse:
    return ServiceResponse(
        error_type=ErrorType.INTEGRITY_ERROR,
        success=False,
        message=str(err)
    )


def handle_database_error(err: DatabaseError) -> ServiceResponse:
    return ServiceResponse(
        error_type=ErrorType.UNKNOWN_ERROR,
        success=False,
        message=str(err)
    )


def handle_unknown_error(err: Exception) -> ServiceResponse:
    return ServiceResponse(
        error_type=ErrorType.UNKNOWN_ERROR,
        success=False,
        message=str(err)
    )


def handle_obj_not_exists_error(err: ObjectDoesNotExist) -> ServiceResponse:
    return ServiceResponse(
        error_type=ErrorType.NOT_FOUND,
        success=False,
        message=str(err)
    )
