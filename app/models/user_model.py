from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .friend_model import Friend


class UserBase(SQLModel):
    """
    User base model containing shared properties
    """
    name: str = Field(max_length=255, index=True)
    status: str = Field(default='Hey there, let\'s digitize our ad processes with Wheel.io')
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(UserBase, table=True):
    """
    Database User model
    """
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    email_verified_at: datetime | None = None
    hashed_password: str
    is_active: bool = Field(default=True)
    friends_sent: list['Friend'] | None = Relationship(
        back_populates='sender',
        sa_relationship_kwargs={
            'foreign_keys': 'Friend.sender_id'
        }
    )
    friends_received: list['Friend'] | None = Relationship(
        back_populates='recipient',
        sa_relationship_kwargs={
            'foreign_keys': 'Friend.recipient_id'
        }
    )
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRegister(SQLModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


class CurrentUser(UserBase):
    id: int
    username: str
    email: EmailStr
    email_verified_at: datetime | None
    is_active: bool
    updated_at: datetime


class UserPublic(UserBase):
    id: int
