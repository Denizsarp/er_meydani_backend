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
import email_verification
from email_verification import Email
import secrets
import datetime
from datetime import datetime, timedelta, timezone
import jwtToken
from jwtToken import TokenOp
import password_validation
from password_validation import PasswordOP


router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

#register user

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def user_register(user_features:schemas.UserCreate, db:Session = Depends(database.get_database)):

    create_data = user_features.model_dump(exclude_unset=True)
    email = create_data["email"].strip().lower()
    username = create_data["username"].strip()

    existing_user_email = db.query(models.User).filter(models.User.email == email).first()
    existing_user_username = db.query(models.User).filter(models.User.username == username).first()

    if existing_user_email:
        raise HTTPException(detail="This email has been registered already!", status_code=status.HTTP_409_CONFLICT)
    if existing_user_username:
        raise HTTPException(detail="This username is already taken!", status_code=status.HTTP_409_CONFLICT)

    pass_score:str = PasswordOP.validate_password(create_data['password'])
    if pass_score:
        raise HTTPException(detail=f"Password Error: {pass_score}", status_code=status.HTTP_409_CONFLICT)
    


    hashed_password = Hash.bcrypt(create_data['password'])

    verification_code:str = str(secrets.randbelow(900000) + 100000)

    new_user = models.User(
        username=create_data['username'].strip(),
        email=create_data['email'].strip().lower(),
        password=hashed_password,
        bio=create_data['bio'] if create_data['bio'] else '',
        profile_photo = create_data['profile_photo'],
        is_verified = False,
        verification_code = verification_code,
        verification_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=30),
        verification_code_resend_limit = datetime.now(timezone.utc) + timedelta(minutes=3)
    )

    Email.email_verification_send(create_data['email'], verification_code)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#User Login endpoint
@router.post('/login', status_code=status.HTTP_200_OK, response_model=dict)
async def user_login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_database)):

    user_info:str = request.username.strip()
    if '@' in user_info:
        user = db.query(models.User).filter(models.User.email == user_info.lower()).first()
    else:
        user = db.query(models.User).filter(models.User.username == user_info).first()


    if not user:
        raise HTTPException(detail='Invalid Credidentals!', status_code=status.HTTP_401_UNAUTHORIZED)

    verify_password = Hash.verify_password(request.password, user.password)

    if not verify_password:
        raise HTTPException(detail="Invalid Credidentals!", status_code=status.HTTP_401_UNAUTHORIZED)


    if not user.is_verified:
        raise HTTPException(detail="Email verification not confirmed!", status_code=status.HTTP_403_FORBIDDEN)

    else:
        #access token yaratmaliyiz!

        access_token = TokenOp.create_access_token(
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




#email verification control
@router.post('/verify-email', status_code=status.HTTP_200_OK, response_model=dict)
async def verify_email(data:schemas.EmailVerification, db:Session = Depends(database.get_database)) -> dict:
    target_user:models.User = db.query(models.User).filter(models.User.email == data.email).first()

    if not target_user:
        raise HTTPException(detail="User not found!", status_code=status.HTTP_404_NOT_FOUND)

    if data.code != target_user.verification_code:
        return {
            'message' : "Verification code is wrong!",
            'status' : "error"
        }

    elif datetime.now(timezone.utc) > target_user.verification_code_expires_at:
        raise HTTPException(detail="Verification code expired!", status_code=status.HTTP_400_BAD_REQUEST)


    else:
        target_user.is_verified = True
        target_user.verification_code = None
        target_user.verification_code_expires_at = None
        target_user.verification_code_resend_limit = None
        db.commit()
        return {
            'message' : "Verificated successfully, you can login!",
            'status' : "success"
        }



#resend email verification code
@router.post('/resend-verification', status_code=status.HTTP_200_OK, response_model=dict)
async def resend_code(data:schemas.ResendVerification, db:Session = Depends(database.get_database)) -> dict:
    target_user = db.query(models.User).filter(models.User.email == data.email).first()
    if not target_user:
        raise HTTPException(detail="User not found!", status_code=status.HTTP_404_NOT_FOUND)
    if target_user.is_verified:
        raise HTTPException(detail="User already verified, you can login.", status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if not datetime.now(timezone.utc) > target_user.verification_code_resend_limit:
        left_time = target_user.verification_code_resend_limit - datetime.now(timezone.utc)
        raise HTTPException(detail=f"Please wait for {left_time}", status_code=status.HTTP_425_TOO_EARLY)
    

    new_code:str = str(secrets.randbelow(900000) + 100000)
    target_user.verification_code = new_code
    target_user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    target_user.verification_code_resend_limit = datetime.now(timezone.utc) + timedelta(minutes=3)
    db.commit()

    Email.email_verification_send(target_user.email, new_code)
    return {
        'message' : "New verification code sent!",
        'status' : 'success'
    }

    




