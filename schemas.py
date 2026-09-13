from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID


# ---------------- USER INPUT ----------------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    bio: Optional[str] = None
    profile_photo:Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    profile_photo: Optional[str] = None


# ---------------- MEMORY INPUT ----------------

class MemoryCreate(BaseModel):
    title: str
    content: str


class MemoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# ---------------- COMMENT INPUT ----------------

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: Optional[str] = None

# ---------------- DISPLAY SCHEMAS ----------------

class UserDisplay(BaseModel):
    username: str
    profile_photo: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class CommentDisplay(BaseModel):
    content: str
    user: UserDisplay

    model_config = {
        "from_attributes": True
    }


class Comment(BaseModel):
    id: UUID
    content: str
    created_at: datetime
    user: UserDisplay

    model_config = {
        "from_attributes": True
    }


class MemoryDisplay(BaseModel):
    title: str
    content: str
    created_at: datetime
    user: UserDisplay
    comments: List[CommentDisplay] = []

    model_config = {
        "from_attributes": True
    }


class Memory(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: datetime
    comments: List[Comment] = []

    model_config = {
        "from_attributes": True
    }


class User(BaseModel):
    id: UUID
    username: str
    #password: str
    email: str
    bio: Optional[str] = None
    profile_photo: Optional[str] = None
    memories: List[Memory] = []

    model_config = {
        "from_attributes": True
    }

class EmailVerification(BaseModel):
    email:str
    code:str


class ResendVerification(BaseModel):
    email:str