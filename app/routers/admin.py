from fastapi import APIRouter, Depends, status

from app import admin_service, service
from app.database import db_dependency
from app.routers.auth import get_current_superuser
from app.schemas import TaskResponse, TaskCreate, AdminUserResponse

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_superuser)])


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency):
    return await admin_service.admin_get_all_tasks(db)

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=AdminUserResponse)
async def get_user(db: db_dependency, user_id: int):
    return await service.get_user(db, user_id)

@router.delete("/todos/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(task_id: int, db: db_dependency):
    return await admin_service.admin_delete_task_by_id(db, task_id)

@router.post("/todos/{target_user_id}", response_model=TaskResponse, status_code=201)
async def create_task(db: db_dependency, target_user_id: int, task: TaskCreate):
    return await admin_service.admin_create_task(db, target_user_id, task)

@router.patch("/users/role/{user_id}", response_model=AdminUserResponse, status_code=200)
async def change_role_by_id(db: db_dependency, user_id: int, is_superuser: bool):
    return await admin_service.change_role_by_id(db, user_id, is_superuser)
