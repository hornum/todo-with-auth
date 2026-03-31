from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from app.schemas import CreateTodo


async def add_task(db: AsyncSession, user_id: int, task: CreateTodo) -> Task:
    new_task = Task(
            title=task.title,
            description=task.description,
            user_id=user_id,
            priority=task.priority,
            is_completed=task.is_completed,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_all_tasks(db: AsyncSession, user_id: int) -> List[Task]:
    stmt = select(Task).where(Task.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_task_by_id(db: AsyncSession, task_id: int) -> Task | None:
    stmt = select(Task).where(Task.id == task_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
