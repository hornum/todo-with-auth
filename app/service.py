from typing import List

from fastapi import HTTPException

import app.dao as dao
from app.models import Task
from app.schemas import CreateTodo


async def create_task(user: dict, task: CreateTodo) -> Task:
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication failed.")
    return await dao.add_task(task, user.get('user_id'))

async def get_all_tasks(user: dict) -> List[Task]:
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication failed.")
    return await dao.get_all_tasks(user.get('user_id'))

async def get_task_by_id(user: dict, task_id: int) -> Task:
    task = await dao.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    if task.user_id != user.get('user_id'):
        raise HTTPException(status_code=404, detail="Authentication failed.")
    return task

async def update_task_status(user, task_id, status) -> Task:
    task = await dao.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    if task.user_id != user.get('user_id'):
        raise HTTPException(status_code=404, detail="Authentication failed.")
    return await dao.update_task_status(task_id, status)

async def delete_task_by_id(user: dict, task_id: int) -> None:
    task = await dao.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    if task.user_id != user.get('user_id'):
        raise HTTPException(status_code=404, detail="Authentication failed.")
    return await dao.delete_task_by_id(task_id)
