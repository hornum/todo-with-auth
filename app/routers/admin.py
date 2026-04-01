from fastapi import APIRouter, Depends, status
from typing import Annotated


from app import admin_service
from app.database import db_dependency
from app.routers.auth import get_current_superuser
from app.schemas import TaskResponse, CreateTodo

router = APIRouter(prefix="/admin", tags=["Admin"])

superuser_dependency = Annotated[dict, Depends(get_current_superuser)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency, current_user: superuser_dependency):
    return await admin_service.admin_get_all_tasks(db)

@router.delete("/todos/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(task_id: int, db: db_dependency, current_user: superuser_dependency):
    return await admin_service.admin_delete_task_by_id(db, task_id)

@router.post("/{target_user_id}", response_model=TaskResponse, status_code=201)
async def create_task(db: db_dependency, target_user_id, current_user: superuser_dependency, task: CreateTodo):
    return await admin_service.admin_create_task(db, target_user_id, task)

# @router.post("/users/admins/{user_id}", status_code=status.HTTP_201_CREATED)
# async def switch_role_by_id(current_user: superuser_dependency, db: db_dependency, user_id: int):
#     if not current_user.get('is_superuser'):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only for superusers")
#     stmt = select(User).where(User.id == user_id)
#     result = db.execute(stmt)