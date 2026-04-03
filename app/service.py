from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.dao as dao
from app.models import Task, User
from app.schemas import CreateTodo, TodoStatusUpdate, ChangePassword
from app.security import verify_password, get_password_hash


async def get_user_task_or_404(db: AsyncSession, user_id: int, task_id: int) -> Task:
    task = await dao.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden.")

    return task

async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await dao.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def create_task(db: AsyncSession, user_id: int, task: CreateTodo) -> Task:
    return await dao.add_task(db, user_id, task)

async def get_all_tasks(db: AsyncSession, user_id: int) -> List[Task]:
    return await dao.get_all_tasks_for_user(db, user_id)

async def get_task_by_id(db: AsyncSession, user_id: int, task_id: int) -> Task:
    task = await get_user_task_or_404(db, user_id, task_id)
    return task

async def update_task_status(db: AsyncSession, user_id: int, task_id: int, status: TodoStatusUpdate) -> Task:
    task = await get_user_task_or_404(db, user_id, task_id)
    task.is_completed = status.is_completed
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task_by_id(db: AsyncSession, user_id: int, task_id: int) -> None:
    task = await get_user_task_or_404(db, user_id, task_id)
    await db.delete(task)
    await db.commit()

async def delete_all_user_tasks(db: AsyncSession, user_id: int) -> None:
    return await dao.delete_all_user_tasks(db, user_id)

async def change_password(db: AsyncSession, user_id: int, pass_verify: ChangePassword) -> None:
    user = await dao.get_user_by_id(db, user_id)
    if not verify_password(pass_verify.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect password")
    user.hashed_password = get_password_hash(pass_verify.new_password)
    await db.commit()
    await db.refresh(user)