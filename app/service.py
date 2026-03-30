from typing import List

import app.dao as dao
from app.models import Task
from app.schemas import CreateTodo


async def create_task(task: CreateTodo, user_id: int) -> Task:
    return await dao.add_task(task, user_id)

async def get_all_tasks(user_id: int) -> List[Task]:
    return await dao.get_all_tasks(user_id)

async def get_task_by_id(task_id: int) -> Task:
    return await dao.get_task_by_id(task_id)

async def update_task_status(task_id, status) -> Task:
    return await dao.update_task_status(task_id, status)