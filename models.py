""""
Database models to be created.
"""

import sqlalchemy
from sqlalchemy import Integer, Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


class User(Base):
    __tablename__  = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, nullable=False)
    email  = Column(Text, nullable=False)
    password = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    profile_photo = Column(Text, nullable=True)

    memories = relationship("Memory", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")




class Memory(Base):
    __tablename__ = "memories"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        nullable=False
    )

    user = relationship("User", back_populates="memories")
    comments = relationship("Comment", back_populates="memory")



class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        nullable=False
    )

    memory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("memory.id"),
        nullable=False
    )

    user = relationship("User", back_populates="comments")


class Like(Base):
    __tablename__ = "likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, nullable=False)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        nullable=False
    )

    memory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("memory.id"),
        nullable=False
    )

    user = relationship("User", back_populates="likes")






