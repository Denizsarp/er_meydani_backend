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
import uuid
from uuid import UUID


router = APIRouter(
    prefix="/users",
    tags=['User']
)


#ASYNC FUNCS--------------------------------------------------------------


@router.get('/',status_code=200, response_model=List[schemas.UserDisplay])
async def search_users(db:Session=Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users


@router.get('/{target_user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserDisplay)
async def get_target_user(target_user_id:UUID, db:Session=Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    target_user = db.query(models.User).filter(models.User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(detail="No User Found!", status_code=404)
    else:
        return target_user



@router.get('/me', status_code=status.HTTP_200_OK, response_model=schemas.UserDisplay)
async def get_your_user(db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)) -> schemas.UserDisplay:
    target_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not target_user:
        raise HTTPException(detail="No User Found!", status_code=404)
    return target_user








@router.delete('/me', status_code=status.HTTP_200_OK, response_model=str)
async def delete_user(db: Session=Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    target_user:schemas.User = current_user if current_user else None
    if target_user:
        if not target_user.id == current_user.id:
            raise HTTPException(detail="No authentication", status_code=status.HTTP_401_UNAUTHORIZED)
        target_id:UUID = current_user.id
        db.query(models.User).filter(models.User.id == target_id).delete(synchronize_session=False)
        db.commit()
        return 'User account deleted successfully!'



@router.patch('/me', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def patch_user(new_features:schemas.UserUpdate, db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    target_user:schemas.User = current_user if current_user else None
    if not target_user.id == current_user.id:
        raise HTTPException(detail="No authentication", status_code=status.HTTP_401_UNAUTHORIZED)


    if target_user:
        user_query:schemas.User = db.query(models.User).filter(models.User.id == target_user.id)
        update_data = new_features.model_dump(exclude_unset=True)

        user_query.update(update_data, synchronize_session=False)
        db.commit()

        return db.query(models.User).filter(models.User.id == target_user.id).first()







    

