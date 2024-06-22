from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .friend import Friend


class User(SQLModel, table=True):
    """
    User model
    """
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    name: str
    hashed_password: str
    is_active: bool = Field(default=True)
    status: str = Field(default='Hey there, let\'s digitize our ad processes with Wheel.io')
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
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
