from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.tasks import router as tasks_router
from app.routers.admin import router as admin_router
from app.routers.users import router as users_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(admin_router)
app.include_router(users_router)