from django.db import IntegrityError, DatabaseError
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from src.projects.dto.tag import TagResponseDTO, TagCreateDTO, TagUpdateDTO
from src.projects.repositories.tag import TagRepository
from src.projects.services.service_responce import ServiceResponse, ErrorType


class TagService:
    def __init__(self):
        self.repository = TagRepository()

    def get_all_tags(self) -> ServiceResponse:
        try:
            tags = self.repository.get_all()
            serializer = TagResponseDTO(tags, many=True)
            return ServiceResponse(data=serializer.data, success=True)

        except DatabaseError as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message=str(e)
            )

        except Exception:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message='Error getting list of tags'
            )

    def get_tag_by_id(self, tag_id: int):
        try:
            tag = self.repository.get_by_id(id_=tag_id)
            serializer = TagResponseDTO(tag)
            return ServiceResponse(data=serializer.data, success=True)

        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND.value,
                message=str(e)
            )

        except DatabaseError as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message=str(e)
            )

        except Exception:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message='Error getting of tag'
            )

    def create_tag(self, tag_data: dict) -> ServiceResponse:
        try:
            serializer = TagCreateDTO(data=tag_data)
            serializer.is_valid(raise_exception=True)

            tag = self.repository.create(**serializer.validated_data)
            serialized_response = TagResponseDTO(tag)
            return ServiceResponse(
                data=serialized_response.data,
                success=True
            )

        except ValidationError as e:
            return ServiceResponse(
                error_type=ErrorType.VALIDATION_ERROR.value,
                success=False,
                message=str(e)
            )

        except IntegrityError as e:
            return ServiceResponse(
                error_type=ErrorType.INTEGRITY_ERROR.value,
                success=False,
                message=str(e)
            )

        except DatabaseError as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message=str(e)
            )

        except Exception as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message=f'Failed to create object {e}'
            )

    def update_tag(self, tag_id: int, tag_data: dict, partial=False):
        try:
            update_serializer = TagUpdateDTO(data=tag_data, partial=partial)

            if not update_serializer.is_valid():
                return ServiceResponse(
                    errors=update_serializer.errors,
                    error_type=ErrorType.VALIDATION_ERROR.value,
                    success=False)

            updated_tag = self.repository.update(
                id_=tag_id,
                **update_serializer.validated_data
            )
            response = TagResponseDTO(updated_tag)
            return ServiceResponse(success=True, data=response.data)

        except ValidationError as e:
            return ServiceResponse(
                error_type=ErrorType.VALIDATION_ERROR.value,
                success=False,
                message=str(e)
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

        except Exception as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message=f'Failed to create object {e}'
            )

    def delete_tag(self, tag_id):
        try:
            self.repository.delete(tag_id)
            return ServiceResponse(success=True)

        except ObjectDoesNotExist as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.NOT_FOUND.value,
                message=str(e)
            )

        except DatabaseError as e:
            return ServiceResponse(
                success=False,
                error_type=ErrorType.UNKNOWN_ERROR.value,
                message=str(e)
            )

        except Exception as e:
            return ServiceResponse(
                error_type=ErrorType.UNKNOWN_ERROR.value,
                success=False,
                message=f'Failed to delete object {e}'
            )
