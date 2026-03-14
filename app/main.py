import uvicorn
from fastapi import FastAPI

from app.routers.auth import router as auth_router


app = FastAPI()
app.include_router(auth_router)

@app.get("/")
async def main():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, reload=True)