from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from typing import List, Optional
import models
import schemas
import database
import hashing # type: ignore
from hashing import Hash # type: ignore
from database import engine, SessionLocal
from sqlalchemy.orm import Session
#import authentication
import oauth2
import uuid
from uuid import UUID


router = APIRouter(
    prefix="/users",
    tags=['User']
)


#ASYNC FUNCS--------------------------------------------------------------

#get all users
@router.get('/',status_code=200, response_model=List[schemas.UserDisplay])
async def search_users(db:Session=Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users





#get your self profile
@router.get('/me', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_your_user(db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)) -> schemas.User:
    target_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not target_user:
        raise HTTPException(detail="No User Found!", status_code=404)
    return target_user






#get user by its ID
@router.get('/{target_user_id}', status_code=status.HTTP_200_OK, response_model=schemas.UserDisplay)
async def get_target_user(target_user_id:UUID, db:Session=Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    target_user = db.query(models.User).filter(models.User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(detail="No User Found!", status_code=404)
    else:
        return target_user




#delete your profile
@router.delete('/me', status_code=status.HTTP_200_OK, response_model=str)
async def delete_user(db: Session=Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    target_user:models.User = current_user if current_user else None

    if target_user:
        if not target_user.id == current_user.id:
            raise HTTPException(detail="No authentication", status_code=status.HTTP_401_UNAUTHORIZED)

        user_memories:List[models.Memory] = list(target_user.memories)
        for current_memory in user_memories:
            current_memory_comments:List[models.Comment] = list(current_memory.comments)
            for target_comment in current_memory_comments:
                db.delete(target_comment)

            db.delete(current_memory)

        user_another_comments:List[models.Comment] = target_user.comments
        for comment in user_another_comments:
            db.delete(comment)
        db.flush()

        db.delete(target_user)
        
        db.commit()
        return 'User account deleted successfully!'
    else:
        raise HTTPException(detail="User not found!", status_code=status.HTTP_404_NOT_FOUND)



#update your profile
@router.patch('/me', status_code=status.HTTP_200_OK, response_model=schemas.UserDisplay)
async def patch_user(new_features:schemas.UserUpdate, db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)) -> schemas.UserDisplay:
    target_user:models.User = current_user if current_user else None

    if not target_user:
        raise HTTPException(detail="User not found!", status_code=status.HTTP_404_NOT_FOUND)
    if not target_user.id == current_user.id:
        raise HTTPException(detail="No authentication", status_code=status.HTTP_401_UNAUTHORIZED)




    if target_user:
        user_query = db.query(models.User).filter(models.User.id == target_user.id)
        update_data = new_features.model_dump(exclude_unset=True)

        if "password" in update_data and update_data['password']:
            update_data['password'] = Hash.bcrypt(update_data['password'])

        user_query.update(update_data, synchronize_session=False)
        db.commit()

        return db.query(models.User).filter(models.User.id == target_user.id).first()







    

