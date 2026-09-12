from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from models import BookModel, UserModel
from schemas import Book, ShowBook, User
from typing import List, Optional
import models
import schemas
import database
import hashing # type: ignore
from hashing import Hash # type: ignore
from datetime import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import authentication
import oauth2
import uuid
from uuid import UUID

router = APIRouter(
    prefix="/memories",
    tags=['Memories']
)

#GET ALL MEMORIES
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.MemoryDisplay])
async def get_all_memories(db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    memories = db.query(models.Memory).all()
    return memories



#GET USER'S MEMORIES
@router.get('/user/{target_user_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.MemoryDisplay])
async def get_user_memories(target_user_id:UUID, db:Session = Depends(database.get_database), current_user:schemas.User = Depends(oauth2.get_current_user)):
    target_user = db.query(models.User).filter(models.User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(detail="User not found!", status_code=status.HTTP_404_NOT_FOUND)

    memories_of_user = db.query(models.Memory).filter(models.Memory.user_id == target_user_id).all()

    return memories_of_user


#GET MEMORIY BY ITS ID
@router.get('/{memory_id}', status_code=status.HTTP_200_OK, response_model=schemas.MemoryDisplay)
async def get_specific_memory(memory_id:UUID, db:Session = Depends(database.get_database), current_user:schemas.User = Depends(oauth2.get_current_user)):
    target_memory = db.query(models.Memory).filter(models.Memory.id == memory_id).first()
    if not target_memory:
        raise HTTPException(detail="Memory not found!", status_code=status.HTTP_404_NOT_FOUND)
    else:
        return target_memory

    
#DELETE MEMORY BY ITS ID
@router.delete('/{memory_id}', status_code=status.HTTP_200_OK, response_model=str)
async def delete_memory(memory_id:UUID, db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    target_memory = db.query(models.Memory).filter(models.Memory.id == memory_id).first()
    if not target_memory:
        raise HTTPException(detail="Memory not found!", status_code=status.HTTP_404_NOT_FOUND)

    else:
            if target_memory.user_id != current_user.id:
                raise HTTPException(detail='You are not authorized for this action!', status_code=status.HTTP_403_FORBIDDEN)
            db.delete(target_memory)
            db.commit()
            return 'removal is successful!'


    
#PATCH MEMORY BY ITS ID
@router.patch('/{memory_id}', status_code=status.HTTP_200_OK, response_model=schemas.Memory)
async def update_memory(memory_id:UUID, new_features:schemas.MemoryUpdate, db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    current_memory:schemas.Memory = db.query(models.Memory).filter(models.Memory.id == memory_id).first()

    if not current_memory:
        raise HTTPException(detail="Memory not found!", status_code=status.HTTP_404_NOT_FOUND)
    
    if not current_memory.user_id == current_user.id:
        raise HTTPException(detail="You don't have authorization for this!", status_code=status.HTTP_403_FORBIDDEN)


    if not current_memory in current_user.memories:
        raise HTTPException(detail="no authentication", status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        update_data = new_features.model_dump(exclude_unset=True)
        memory_query = db.query(models.Memory).filter(models.Memory.id == memory_id)

        memory_query.update(update_data, synchronize_session=False)
        
        db.commit()

        return db.query(models.Memory).filter(models.Memory.id == memory_id).first()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=str)
async def create_new_memory(features:schemas.MemoryCreate, db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    create_data = features.model_dump(exclude_unset=True)
    if not create_data['title']:
        raise HTTPException(detail="The memory should have title!", status_code=status.HTTP_204_NO_CONTENT)
    if not create_data['content']:
        raise HTTPException(detail="The memory should have content!", status_code=status.HTTP_204_NO_CONTENT)
    date_of_memory = datetime.now()

    create_data['created_at'] = date_of_memory

    new_memory = models.Memory(
        title=create_data['title'],
        content=create_data['content'],
        created_at=date_of_memory,
        user_id = current_user.id
    )

    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)

    return 'New Memory succesfully created!'


    





