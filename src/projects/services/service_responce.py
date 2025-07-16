from enum import Enum
from typing import Any, Dict, Optional


class ErrorType(str, Enum):
    NOT_FOUND = "объект не найден"
    VALIDATION_ERROR = "ошибка валидации данных"
    INTEGRITY_ERROR = "нарушение целостности данных"
    UNKNOWN_ERROR = "неизвестная ошибка"

class ServiceResponse:
    def __init__(
        self,
        success: bool,
        data: Optional[Any] = None,
        errors: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
        error_type: Optional[ErrorType] = None
    ) -> None:
        self.success: bool = success
        self.data: Optional[Any] = data
        self.errors: Dict[str, Any] = errors or {}
        self.message: Optional[str] = message
        self.error_type: Optional[ErrorType] = error_type

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"success": self.success}

        if self.data is not None:
            result["data"] = self.data
        if self.errors:
            result["errors"] = self.errors
        if self.message is not None:
            result["message"] = self.message
        if self.error_type is not None:
            result["error_type"] = self.error_type.value

        return result
