from fastapi import APIRouter, Depends, status
from typing import Annotated

import app.service as service
from app.database import db_dependency
from app.models import User
from app.routers.auth import get_current_user
from app.schemas import PasswordChange, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])

user_dependency = Annotated[User, Depends(get_current_user)]

@router.get("/me", response_model=UserResponse)
async def get_user(db: db_dependency, user: user_dependency):
    return await service.get_user(db, user.id)

@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency, user: user_dependency, password_verify: PasswordChange):
    return await service.change_password(db, user.id, password_verify)
