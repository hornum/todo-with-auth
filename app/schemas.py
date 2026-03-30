from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_superuser: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateTodo(BaseModel):
    title: str = Field(max_length=200)
    description: Optional[str] = Field(max_length=300)
    is_completed: Optional[bool] = False
    priority: int = Field(gt=0, lt=6)

class TodoStatusUpdate(BaseModel):
    is_done: bool