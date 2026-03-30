from typing import List

from sqlalchemy import select

from app.database import async_session_maker
from app.models import Task
from app.schemas import CreateTodo, TodoStatusUpdate


async def add_task(task: CreateTodo, user_id: int) -> Task:
    async with async_session_maker() as session:
        new_task = Task(
            title=task.title,
            description=task.description,
            user_id=user_id,
            priority=task.priority,
            is_completed=task.is_completed,
        )
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
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
        task = result.scalar_one_or_none()
        if task is None:
            return None
        task.is_completed = status.is_completed
        await session.commit()
        await session.refresh(task)
        return task

async def delete_task_by_id(task_id: int) -> None:
    async with async_session_maker() as session:
        stmt = select(Task).where(Task.id == task_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        await session.delete(task)