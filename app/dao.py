from typing import List

from sqlalchemy import select

from app.database import async_session_maker
from app.models import Task
from app.schemas import CreateTodo, TodoStatusUpdate


async def add_task(task: CreateTodo, user_id: int):
    async with async_session_maker() as session:
        new_task = Task(
            title=task.title,
            description=task.description,
            user_id=user_id,
            priority=task.priority,
        )
        session.add(new_task)
        await session.commit()
        session.refresh(new_task)
        return new_task

async def get_all_tasks(user_id: int) -> List[Task]:
    async with async_session_maker() as session:
        stmt = select(Task).where(Task.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_task_by_id(task_id: int) -> Task:
    async with async_session_maker() as session:
        stmt = select(Task).where(Task.id == task_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def update_task_status(task_id: int, status: TodoStatusUpdate) -> Task:
    async with async_session_maker() as session:
        stmt = select(Task).where(Task.id == task_id)
        result = await session.execute(stmt)
        old_task = result.scalar_one_or_none()
        new_task = Task(
            title = old_task.title,
            description = old_task.description,
            user_id = old_task.user_id,
            priority = old_task.priority,
            created_at = old_task.created_at,
        )
