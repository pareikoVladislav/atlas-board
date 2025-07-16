# from typing import Optional
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from django.db import transaction
# from enum import Enum
# from dataclasses import dataclass
#
#
# # Enums and Data Classes
# class ErrorType(Enum):
#     NOT_FOUND = "not_found"
#     UNKNOWN_ERROR = "unknown_error"
#
#
# @dataclass
# class ServiceResponse:
#     success: bool
#     error_type: Optional[ErrorType] = None
#     error_message: Optional[str] = None
#
#
# # Repository
# class BaseRepository:
#     @staticmethod
#     @transaction.atomic
#     def delete(id_: int, model) -> None:
#         try:
#             instance = model.objects.get(id=id_)
#             instance.delete()
#         except model.DoesNotExist:
#             raise ValueError(f"{model.__name__} with id {id_} not found")
#
#
# class ProjectRepository(BaseRepository):
#     def delete(self, id_: int) -> None:
#         from src.projects.models.project import Project
#         super().delete(id_, Project)
#
#
# # Service
# class ProjectService:
#     def __init__(self):
#         self.repository = ProjectRepository()
#
#     def delete_project(self, project_id: int) -> ServiceResponse:
#         try:
#             self.repository.delete(project_id)
#             return ServiceResponse(success=True)
#         except ValueError as e:
#             return ServiceResponse(
#                 success=False,
#                 error_type=ErrorType.NOT_FOUND,
#                 error_message=str(e)
#             )
#         except Exception as e:
#             return ServiceResponse(
#                 success=False,
#                 error_type=ErrorType.UNKNOWN_ERROR,
#                 error_message=str(e)
#             )
#
#
# # View
# @api_view(['DELETE'])
# def delete_project(request, project_id: int) -> JsonResponse:
#     service = ProjectService()
#     response = service.delete_project(project_id)
#
#     if response.success:
#         return JsonResponse({}, status=204)
#     elif response.error_type == ErrorType.NOT_FOUND:
#         return JsonResponse({"error": response.error_message}, status=404)
