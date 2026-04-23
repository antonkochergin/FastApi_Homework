class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


# ============ Общие ошибки БД ============
class DatabaseOperationError(BaseDatabaseException):
    """Общая ошибка операции с БД"""
    pass


# ============ Исключения для пользователей ============
class UserNotFoundException(BaseDatabaseException):
    pass


class UserAlreadyExistsException(BaseDatabaseException):
    pass


# ============ Исключения для постов ============
class PostNotFoundException(BaseDatabaseException):
    pass


# ============ Исключения для комментариев ============
class CommentNotFoundException(BaseDatabaseException):
    pass


class CommentAuthorNotFoundExceptionDB(BaseDatabaseException):
    pass


class CommentPostNotFoundExceptionDB(BaseDatabaseException):
    pass


class CommentIntegrityError(BaseDatabaseException):
    pass


# ============ Исключения для локаций ============
class LocationNotFoundException(BaseDatabaseException):
    pass


class LocationAlreadyExistsException(BaseDatabaseException):
    pass

# ============ Исключения для категорий ============
class CategoryNotFoundException(BaseDatabaseException):
    pass


class CategoryAlreadyExistsException(BaseDatabaseException):
    pass

# ============ Исключения для постов ============
class PostNotFoundException(BaseDatabaseException):
    pass


class PostAuthorNotFoundExceptionDB(BaseDatabaseException):
    pass


class PostCategoryNotFoundExceptionDB(BaseDatabaseException):
    pass


class PostLocationNotFoundExceptionDB(BaseDatabaseException):
    pass