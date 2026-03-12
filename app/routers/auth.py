from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.testing.pickleable import User

from app.schemas import UserRegister

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == user_data.email)
    existing_user = db.execute(stmt).one_or_none()
    if existing_user: