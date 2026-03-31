from typing import Optional
from pydantic import BaseModel, EmailStr, Field


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