from typing import Optional, Any


class AppException(Exception):
    """Базовое исключение приложения"""
    def __init__(
        self,
        message: str,
        code: str = "app_error",
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)