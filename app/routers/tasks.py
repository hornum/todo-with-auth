from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

import app.service as service
from app.database import db_dependency
from app.schemas import CreateTodo, TodoStatusUpdate
from app.routers.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def get_all_tasks(db: db_dependency, current_user: user_dependency):
    return await service.get_all_tasks(db, current_user.get("user_id"))

@router.get("/{task_id}")
async def get_task_by_id(db: db_dependency, current_user: user_dependency, task_id: int):
    return await service.get_task_by_id(db, current_user.get("user_id"), task_id)

@router.post("/")
async def create_task(db: db_dependency, current_user: user_dependency, task: CreateTodo):
    return await service.create_task(db, current_user.get("user_id"), task)

@router.patch("/{task_id}/status")
async def update_task(db: db_dependency, current_user: user_dependency, task_id: int, status: TodoStatusUpdate):
    return await service.update_task_status(db, current_user.get("user_id"), task_id, status)

@router.delete("/{task_id}")
async def delete_task(db: db_dependency, current_user: user_dependency, task_id: int):
    return await service.delete_task_by_id(db, current_user.get("user_id"), task_id)