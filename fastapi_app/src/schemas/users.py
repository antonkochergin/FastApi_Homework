from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    """Базовая модель пользователя"""
    username: str = Field(min_length=3, max_length=150, description="Логин")
    email: EmailStr = Field(description="Email")
    first_name: str | None = Field(None, max_length=150, description="Имя")
    last_name: str | None = Field(None, max_length=150, description="Фамилия")

class User(UserBase):
    """ Для чтения без поролей из БД"""
    id: int
    model_config = ConfigDict(from_attributes=True)