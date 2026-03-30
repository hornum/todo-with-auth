from collections.abc import AsyncGenerator
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.pickleable import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated

from app.config import settings
from app.database import async_session_maker
from app.schemas import UserRegister, Token
from app.models import User
from app.security import get_password_hash, verify_password
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Invalid token')
        return {'username': username, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token')


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


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
            username=user_data.username,
            hashed_password=hashed_password,
            is_superuser=user_data.is_superuser,
            created_at=datetime.now(timezone.utc),
        )
        session.add(new_user)
        await session.commit()

@router.post("/token", response_model=Token)
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

            return {"access_token": token, 'token_type': 'bearer'}

    raise HTTPException(status_code=400, detail="Incorrect email or password")