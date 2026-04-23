class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


# ============ Исключения для пользователей ============
class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' не найден"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)
        super().__init__(detail=detail)


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с username='{username}' не найден"

    def __init__(self, username: str) -> None:
        detail = self._exception_text_template.format(username=username)
        super().__init__(detail=detail)


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с ID='{user_id}' не найден"

    def __init__(self, user_id: int) -> None:
        detail = self._exception_text_template.format(user_id=user_id)
        super().__init__(detail=detail)


class UserLoginIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' уже существует"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)
        super().__init__(detail=detail)


class UserUsernameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с username='{username}' уже существует"

    def __init__(self, username: str) -> None:
        detail = self._exception_text_template.format(username=username)
        super().__init__(detail=detail)


class UserEmailIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с email='{email}' уже существует"

    def __init__(self, email: str) -> None:
        detail = self._exception_text_template.format(email=email)
        super().__init__(detail=detail)


# ============ Исключения для комментариев ============
class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с ID='{comment_id}' не найден"

    def __init__(self, comment_id: int) -> None:
        detail = self._exception_text_template.format(comment_id=comment_id)
        super().__init__(detail=detail)


class CommentAuthorNotFoundException(BaseDomainException):
    _exception_text_template = "Автор с ID='{author_id}' не найден"

    def __init__(self, author_id: int) -> None:
        detail = self._exception_text_template.format(author_id=author_id)
        super().__init__(detail=detail)


class CommentPostNotFoundException(BaseDomainException):
    _exception_text_template = "Пост с ID='{post_id}' не найден"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail)


class CommentTextEmptyException(BaseDomainException):
    _exception_text_template = "Текст комментария не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


# ============ Исключения для локаций ============
class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Локация с ID='{location_id}' не найдена"

    def __init__(self, location_id: int) -> None:
        detail = self._exception_text_template.format(location_id=location_id)
        super().__init__(detail=detail)


class LocationNameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Локация с названием='{name}' уже существует"

    def __init__(self, name: str) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail)


class LocationNameEmptyException(BaseDomainException):
    _exception_text_template = "Название локации не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)

# ============ Исключения для категорий ============
class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с ID='{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail)


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория со slug='{slug}' не найдена"

    def __init__(self, slug: str) -> None:
        detail = self._exception_text_template.format(slug=slug)
        super().__init__(detail=detail)


class CategorySlugIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория со slug='{slug}' уже существует"

    def __init__(self, slug: str) -> None:
        detail = self._exception_text_template.format(slug=slug)
        super().__init__(detail=detail)


class CategoryTitleIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория с названием='{title}' уже существует"

    def __init__(self, title: str) -> None:
        detail = self._exception_text_template.format(title=title)
        super().__init__(detail=detail)


class CategoryTitleEmptyException(BaseDomainException):
    _exception_text_template = "Название категории не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class CategorySlugEmptyException(BaseDomainException):
    _exception_text_template = "Slug категории не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)

# ============ Исключения для постов ============
class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пост с ID='{post_id}' не найден"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail)


class PostAuthorNotFoundException(BaseDomainException):
    _exception_text_template = "Автор с ID='{author_id}' не найден"

    def __init__(self, author_id: int) -> None:
        detail = self._exception_text_template.format(author_id=author_id)
        super().__init__(detail=detail)


class PostCategoryNotFoundException(BaseDomainException):
    _exception_text_template = "Категория с ID='{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail)


class PostLocationNotFoundException(BaseDomainException):
    _exception_text_template = "Локация с ID='{location_id}' не найдена"

    def __init__(self, location_id: int) -> None:
        detail = self._exception_text_template.format(location_id=location_id)
        super().__init__(detail=detail)


class PostTitleEmptyException(BaseDomainException):
    _exception_text_template = "Заголовок поста не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class PostTextEmptyException(BaseDomainException):
    _exception_text_template = "Содержание поста не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class WrongPasswordException(BaseDomainException):
    _exception_text_template = "Неверный пароль для пользователя с логином='{login}'"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)
        super().__init__(detail=detail)