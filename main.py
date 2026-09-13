"""
Routers, endpoints and fastAPI operations will be here.
"""
from fastapi import FastAPI, status
import models
import schemas
import database
import hashing # type: ignore
from database import engine, SessionLocal, Base
from routers import auth, comments, users, memories


app = FastAPI(
    title="Er Meydani API",
    version="1.0.0"
)

Base.metadata.create_all(bing=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(memories.router)
app.include_router(comments.router)


#essential main get method

@app.get('/', status_code=status.HTTP_200_OK, response_model=dict)
async def root()->dict:
    return {
        'message' : "Er Meydani API is running succesfully!",
        'status' : "success"
    }