from fastapi import status


class BaseDomainException(Exception):
    def __init__(self, detail: str | None = None, status_code: None = None) -> None:
        self._detail = detail
        self._status_code = status_code

    def get_detail(self) -> str:
        return self._detail

    def get_status_code(self) -> status:
        return self._status_code


class CategoryNotFoundException(BaseDomainException):
    _text_template = "Category with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class CategoryNotFoundBySlugException(BaseDomainException):
    _text_template = "Category with slug '{slug}' not found"

    def __init__(self, slug: str) -> None:
        self._text_template = self._text_template.format(slug=slug)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class CategoryWithSlugAlreadyExistException(BaseDomainException):
    _text_template = "Category with slug '{slug}' already exist"

    def __init__(self, slug: str) -> None:
        self._text_template = self._text_template.format(slug=slug)

        super().__init__(detail=self._text_template, status_code=status.HTTP_409_CONFLICT)


class CommentNotFoundException(BaseDomainException):
    _text_template = "Comment with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class LocationNotFoundException(BaseDomainException):
    _text_template = "Location with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class LocationNotFoundByNameException(BaseDomainException):
    _text_template = "Location with name '{name}' not found"

    def __init__(self, name: str) -> None:
        self._text_template = self._text_template.format(name=name)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class LocationWithNameAlreadyExistException(BaseDomainException):
    _text_template = "Location with name '{name}' already exist"

    def __init__(self, name: str) -> None:
        self._text_template = self._text_template.format(name=name)

        super().__init__(detail=self._text_template, status_code=status.HTTP_409_CONFLICT)


class UserNotFoundException(BaseDomainException):
    _text_template = "User with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class UserNotFoundByUsernameException(BaseDomainException):
    _text_template = "User with username '{username}' not found"

    def __init__(self, username: str) -> None:
        self._text_template = self._text_template.format(username=username)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class UserNotFoundByEmailException(BaseDomainException):
    _text_template = "User with email '{email}' not found"

    def __init__(self, email: str) -> None:
        self._text_template = self._text_template.format(email=email)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class UserWithUsernameAlreadyExistException(BaseDomainException):
    _text_template = "User with username '{username}' already exist"

    def __init__(self, username: str) -> None:
        self._text_template = self._text_template.format(username=username)

        super().__init__(detail=self._text_template, status_code=status.HTTP_409_CONFLICT)


class UserWithEmailAlreadyExistException(BaseDomainException):
    _text_template = "User with email '{email}' already exist"

    def __init__(self, email: str) -> None:
        self._text_template = self._text_template.format(email=email)

        super().__init__(detail=self._text_template, status_code=status.HTTP_409_CONFLICT)


class PostNotFoundException(BaseDomainException):
    _text_template = "Post with ID '{id}' not found"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(id=id)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)


class InvalidPasswordException(BaseDomainException):
    _text_template = "Invalid password"

    def __init__(self) -> None:
        self._text_template = self._text_template

        super().__init__(detail=self._text_template, status_code=status.HTTP_401_UNAUTHORIZED)


class DomainPermissionDeniedException(BaseDomainException):
    _text_template = "You can only {method} your own {model}"

    def __init__(self, method: str, model: str) -> None:
        self._text_template = self._text_template.format(method=method, model=model)

        super().__init__(detail=self._text_template, status_code=status.HTTP_403_FORBIDDEN)


class NotEnoughRightsException(BaseDomainException):
    _text_template = "{username} don't have enough rights for this action"

    def __init__(self, username: str) -> None:
        self._text_template = self._text_template.format(username=username)

        super().__init__(detail=self._text_template, status_code=status.HTTP_403_FORBIDDEN)


class UploadFileIsNotImageException(BaseDomainException):
    _text_template = "Unknow image extension"

    def __init__(self) -> None:
        super().__init__(detail=self._text_template, status_code=status.HTTP_400_BAD_REQUEST)


class PostHasNoImageException(BaseDomainException):
    _text_template = "Post {post_id} has no image"

    def __init__(self, id: int) -> None:
        self._text_template = self._text_template.format(post_id=id)

        super().__init__(detail=self._text_template, status_code=status.HTTP_404_NOT_FOUND)
