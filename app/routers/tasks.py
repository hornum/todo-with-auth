from fastapi import APIRouter

import app.service as service
from app.schemas import CreateTodo, TodoStatusUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
async def get_all_tasks(user_id: int):
    return await service.get_all_tasks(user_id)

@router.get("/{task_id}")
async def get_task_by_id(task_id: int):
    return await service.get_task_by_id(task_id)

@router.post("/")
async def create_task(task: CreateTodo, user_id: int):
    return await service.create_task(task, user_id)

@router.patch("/{task_id}/status")
async def update_task(task_id: int, status: TodoStatusUpdate):
    return await service.update_task_status(task_id, status)
