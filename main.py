"""
Routers, endpoints and fastAPI operations will be here.
"""
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from models import BookModel, UserModel
from schemas import Book, ShowBook, User
from typing import List, Optional
import models
import schemas
import database
import hashing # type: ignore
from hashing import Hash # type: ignore
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import authentication
import oauth2


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(authentication.router)

@app.get('/users/{user_id}', status_code=200, response_model=schemas.UserDisplay, tags=['users'])
async def get_single_user(user_id:int, db:Session=Depends(database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User Not Found!")
    return target_user

