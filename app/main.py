import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def main():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, reload=True)