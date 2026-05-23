from fastapi import HTTPException

from core.exceptions.domain_exceptions import BaseDomainException


class BaseApiException(HTTPException):
    def __init__(self, exception: BaseDomainException) -> None:
        super().__init__(status_code=exception.get_status_code(), detail=exception.get_detail())


class NotFoundByFieldException(BaseApiException):
    def __init__(self, exception: BaseDomainException) -> None:
        super().__init__(exception=exception)


class AlreadyExistWithFieldException(BaseApiException):
    def __init__(self, exception: BaseDomainException) -> None:
        super().__init__(exception=exception)


class PermissionDeniedException(BaseApiException):
    def __init__(self, exception: BaseDomainException) -> None:
        super().__init__(exception=exception)


class ImageException(BaseApiException):
    def __init__(self, exception: BaseDomainException) -> None:
        super().__init__(exception=exception)
