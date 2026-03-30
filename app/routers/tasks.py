from fastapi import APIRouter, Depends
from typing import Annotated

import app.service as service
from app.schemas import CreateTodo, TodoStatusUpdate
from app.routers.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def get_all_tasks(user: user_dependency):
    return await service.get_all_tasks(user)

@router.get("/{task_id}")
async def get_task_by_id(user: user_dependency, task_id: int):
    return await service.get_task_by_id(user, task_id)

@router.post("/")
async def create_task(user: user_dependency, task: CreateTodo):
    return await service.create_task(user, task)

@router.patch("/{task_id}/status")
async def update_task(user: user_dependency, task_id: int, status: TodoStatusUpdate):
    return await service.update_task_status(user, task_id, status)

@router.delete("/{task_id}")
async def delete_task(user: user_dependency, task_id: int):
    return await service.delete_task_by_id(user, task_id)