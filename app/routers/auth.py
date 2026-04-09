from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import or_, select

from app.config import settings
from app.database import db_dependency
from app.models import User
from app.schemas import Token, UserCreate
from app.security import get_password_hash, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def create_access_token(username: str, user_id: int, is_superuser: bool, expires_delta: timedelta) -> str:
    encode = {"sub": username, "id": user_id, "is_superuser": is_superuser}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: db_dependency,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")
        if username is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await db.get(User, user_id)
    if user is None or user.username != username:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


async def get_current_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only for superusers")
    return current_user


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: db_dependency) -> None:
    query = select(User).where(
        or_(
            User.email == user_data.email,
            User.username == user_data.username
        )
    )
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        is_superuser=False,
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_user)
    await db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user and verify_password(
        plain_password=form_data.password,
        hashed_password=existing_user.hashed_password,
    ):
        if not existing_user.is_active:
            raise HTTPException(status_code=403, detail="Inactive user")
        token = create_access_token(
            existing_user.username,
            existing_user.id,
            existing_user.is_superuser,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Incorrect username or password")
