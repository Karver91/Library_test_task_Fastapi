import uvicorn
from fastapi import FastAPI

from app.routes import router

app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run("app.main:app", host="127.0.0.1", reload=True, port=8000)
