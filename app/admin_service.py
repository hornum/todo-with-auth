from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.dao as dao
from app.models import Task
from app.schemas import CreateTodo


async def admin_get_all_tasks(db: AsyncSession) -> List[Task]:
    return await dao.get_all_tasks(db)

async def admin_delete_task_by_id(db: AsyncSession, task_id: int) -> None:
    task = await dao.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()

async def admin_create_task(db: AsyncSession, target_user_id: int, task: CreateTodo) -> Task:
    return await dao.add_task(db, target_user_id, task)