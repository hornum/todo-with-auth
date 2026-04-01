from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
from typing import Annotated

from app.config import settings
from app.database import db_dependency
from app.schemas import UserRegister, Token
from app.models import User
from app.security import get_password_hash, verify_password
from jose import jwt, JWTError


router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(username: str, user_id: int, is_superuser: bool, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'is_superuser': is_superuser}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        is_superuser: bool = payload.get('is_superuser')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Invalid token')
        return {'username': username, 'user_id': user_id, 'is_superuser': is_superuser}
    except JWTError:
        raise credentials_exception

async def get_current_superuser(current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user.get("is_superuser"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only for superusers")
    return current_user

@router.post("/register")
async def register_user(user_data: UserRegister, db: db_dependency) -> None:
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email = user_data.email,
        username = user_data.username,
        hashed_password = hashed_password,
        is_superuser = False,
        created_at = datetime.now(timezone.utc),
    )
    db.add(new_user)
    await db.commit()

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
            token = create_access_token(
                existing_user.username,
                existing_user.id,
                existing_user.is_superuser,
                expires_delta=timedelta(minutes=15)
            )

            return {"access_token": token, 'token_type': 'bearer'}

    raise HTTPException(status_code=401, detail="Incorrect username or password")
