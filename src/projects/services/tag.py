from src.projects.dto.tag import TagResponseDTO, TagCreateDTO, TagUpdateDTO
from src.projects.repositories.tag import TagRepository
from src.projects.services.service_responce import ServiceResponse
from src.shared.exception_handlers import handle_service_error


class TagService:
    def __init__(self):
        self.repository = TagRepository()

    def get_all_tags(self) -> ServiceResponse:
        try:
            tags = self.repository.get_all()
            response = TagResponseDTO(tags, many=True)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def get_tag_by_id(self, tag_id: int):
        try:
            tag = self.repository.get_by_id(id_=tag_id)
            response = TagResponseDTO(tag)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def create_tag(self, tag_data: dict) -> ServiceResponse:
        try:
            serializer = TagCreateDTO(data=tag_data)
            serializer.is_valid(raise_exception=True)

            tag = self.repository.create(**serializer.validated_data)
            response = TagResponseDTO(tag)

            return ServiceResponse(data=response.data, success=True)

        except Exception as e:
            return handle_service_error(e)

    def update_tag(self, tag_id: int, tag_data: dict, partial=False):
        try:
            serializer = TagUpdateDTO(data=tag_data, partial=partial)
            serializer.is_valid(raise_exception=True)

            updated_tag = self.repository.update(
                id_=tag_id,
                **serializer.validated_data
            )
            response = TagResponseDTO(updated_tag)

            return ServiceResponse(data=response.data, success=True, )

        except Exception as e:
            return handle_service_error(e)

    def delete_tag(self, tag_id):
        try:
            self.repository.delete(tag_id)
            return ServiceResponse(success=True)

        except Exception as e:
            return handle_service_error(e)
