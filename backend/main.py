from fastapi import FastAPI
from backend.routers import users
from backend.crud.database import init_db

app = FastAPI()


# Automatically creates the database tables - Change for production
@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(users.router)


@app.get("/")
def hello():
    return {"message": "Hello World"}
