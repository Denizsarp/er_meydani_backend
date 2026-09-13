from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
import models
import schemas
import database
import hashing
from hashing import Hash
from database import engine, SessionLocal
from sqlalchemy.orm import Session
#import authentication
import oauth2
import bcrypt


router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

#register user

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def user_register(user_features:schemas.UserCreate, db:Session = Depends(database.get_database)):
    create_data = user_features.model_dump(exclude_unset=True)
    existing_user_email = db.query(models.User).filter(models.User.email == user_features.email).first()
    existing_user_username = db.query(models.User).filter(models.User.username == user_features.username).first()

    if existing_user_email:
        raise HTTPException(detail="This email has been registered already!", status_code=status.HTTP_409_CONFLICT)
    if existing_user_username:
        raise HTTPException(detail="This username is already taken!", status_code=status.HTTP_409_CONFLICT)

    hashed_password = Hash.bcrypt(create_data['password'])

    new_user = models.User(
        username=create_data['username'],
        email=create_data['email'],
        password=hashed_password,
        bio=create_data['bio'],
        profile_photo = create_data['profile_photo']
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#User Login endpoint
@router.post('/login', status_code=status.HTTP_200_OK, response_model=dict)
async def user_login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_database)):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(detail='Invalid Credidentals!', status_code=status.HTTP_401_UNAUTHORIZED)

    verify_status = Hash.verify_password(request.password, user.password)

    if not verify_status:
        raise HTTPException(detail="Invalid Credidentals!", status_code=status.HTTP_401_UNAUTHORIZED)

    else:
        #access token yaratmaliyiz!

        access_token = oauth2.create_access_token(
            data={"sub": str(user.id)} #(user id bazli access token yarattik!)
        )

    return {
        "access_token" : access_token,
        "token_type" : "bearer" 
    }


#user delete
@router.delete('/delete', status_code=status.HTTP_200_OK, response_model=str)
async def delete_user(db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)) -> str:
    target_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not target_user:
        raise HTTPException(detail="user not found!", status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(target_user)
    db.commit()

    return "your account has been deleted successfully!"

