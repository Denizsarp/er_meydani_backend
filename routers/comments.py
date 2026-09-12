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
from datetime import datetime


router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)


#Get Comments of spesific memory
@router.get('/{memory_id}', status_code=status.HTTP_200_OK, response_model=List[schemas.CommentDisplay])
async def get_comments(memory_id:UUID, db:Session = Depends(database.get_database), current_user: models.User = Depends(oauth2.get_current_user)):
    target_memory:schemas.Memory = db.query(models.Memory).filter(models.Memory.id == memory_id).first()
    if not target_memory:
        raise HTTPException(detail="no memory found!", status_code=status.HTTP_404_NOT_FOUND)

    comments = target_memory.comments

    if comments:
        return comments
    else:
        raise HTTPException(detail="no comment found!", status_code=status.HTTP_404_NOT_FOUND)


#Post Comment
@router.post('/{memory_id}', status_code=status.HTTP_201_CREATED, response_model=str)
async def post_comment(memory_id:UUID, features:schemas.CommentCreate, db:Session = Depends(database.get_database), current_user: models.User = Depends(oauth2.get_current_user)):
    create_data = features.model_dump(exclude_unset=True)
    if not create_data['content'].strip():
        raise HTTPException(detail="Blank comment!", status_code=status.HTTP_400_BAD_REQUEST)

    memory_to_create = db.query(models.Memory).filter(models.Memory.id == memory_id).first()

    if not memory_to_create:
        raise HTTPException(detail="Memory not found!", status_code=status.HTTP_404_NOT_FOUND)

    new_comment = models.Comment(
        content = create_data['content'],
        created_at = datetime.now(),
        user_id=current_user.id,
        memory_id=memory_id

    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return 'comment succesfully created!'


#Delete comment by its id
@router.delete('/{comment_id}', status_code=status.HTTP_200_OK, response_model=str)
async def delete_comment(comment_id:UUID, db:Session = Depends(database.get_database), current_user:models.User = Depends(oauth2.get_current_user)):
    target_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    if not target_comment:
        raise HTTPException(detail="Comment not found!", status_code=status.HTTP_404_NOT_FOUND)
    elif target_comment.user_id != current_user.id:
        raise HTTPException(detail="You can not do this action!", status_code=status.HTTP_403_FORBIDDEN)

    db.delete(target_comment)
    db.commit()
    return "removal is successful!"

@router.patch('/update/{target_id}', status_code=status.HTTP_200_OK, response_model=schemas.CommentDisplay)
async def update_comment(target_id:UUID, new_features:schemas.CommentUpdate, db:Session = Depends(database.get_database), current_user : models.User = Depends(oauth2.get_current_user)):
    update_features = new_features.model_dump(exclude_unset=True)

    if update_features['content'] == '':
        raise HTTPException('Comment can not be empty!', status_code=status.HTTP_406_NOT_ACCEPTABLE)

    target_comment = db.query(models.Comment).filter(models.Comment.id == target_id).first()
    if not target_comment:
        raise HTTPException(detail='comment not found!', status_code=status.HTTP_404_NOT_FOUND)
    elif target_comment.user_id != current_user.id:
        raise HTTPException(detail="You are not authorized for this action", status_code=status.HTTP_403_FORBIDDEN)

    target_query = db.query(models.Comment).filter(models.Comment.id == target_id)

    target_query.update(update_features, synchronize_session=False)
    db.commit()
    return db.query(models.Comment).filter(models.Comment.id == target_id).first()


    