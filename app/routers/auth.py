from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql.functions import user
from sqlalchemy.testing.pickleable import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated

from app.config import settings
from app.database import async_session_maker
from app.schemas import UserRegister
from app.models import User
from app.security import get_password_hash, verify_password
from jose import jwt


router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = 'HS256'

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register")
async def register_user(user_data: UserRegister) -> None:
    async with async_session_maker() as session:
        query = select(User).where(User.email == user_data.email)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password= hashed_password,
            created_at=datetime.now(timezone.utc),
        )
        session.add(new_user)
        await session.commit()

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        if verify_password(
                plain_password=form_data.password,
                hashed_password=existing_user.hashed_password
        ):
            token = create_access_token(existing_user.username, existing_user.id, expires_delta=timedelta(minutes=15))
            return {"token": token}

    raise HTTPException(status_code=400, detail="Incorrect email or password")