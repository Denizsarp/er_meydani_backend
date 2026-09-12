from datetime import datetime
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwtToken
import database
import models
import schemas


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(data:str = Depends(oauth2_scheme), db:Session = Depends(database.get_database())) -> models.User:
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authorized!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    current_user_id = jwtToken.verify_token(
        data,
        exc
    )

    user_in_db = db.query(models.User).filter(models.User.id == current_user_id).first()

    if not user_in_db:
        raise exc
    else:
        return user_in_db