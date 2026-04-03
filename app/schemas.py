import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateTodo(BaseModel):
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=200)
    is_completed: bool = False
    priority: int = Field(gt=0, lt=6)

class TodoStatusUpdate(BaseModel):
    is_completed: bool

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: int
    is_completed: bool
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class ChangePassword(BaseModel):
    password: str
    new_password: str
