""""
Database models to be created.
"""

import sqlalchemy
from sqlalchemy import Integer, Column, String, Text, ForeignKey, DateTime, Boolean
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

    is_verified = Column(Boolean, default=False, nullable=False)
    verification_code = Column(String, nullable=True)
    verification_code_expires_at = Column(DateTime(timezone=True), nullable=True)
    verification_code_resend_limit = Column(DateTime(timezone=True), nullable=True)

    memories = relationship("Memory", back_populates="user")
    comments = relationship("Comment", back_populates="user")




class Memory(Base):
    __tablename__ = "memories"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
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
        ForeignKey("users.id"),
        nullable=False
    )

    memory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("memories.id"),
        nullable=False
    )

    user = relationship("User", back_populates="comments")
    memory = relationship("Memory", back_populates="comments")







