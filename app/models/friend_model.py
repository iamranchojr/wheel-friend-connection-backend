from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user_model import User


class FriendStatus(str, Enum):
    Pending: str = 'Pending'
    Accepted: str = 'Accepted'
    Rejected: str = 'Rejected'


class Friend(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: FriendStatus = Field(default=FriendStatus.Pending.value)

    sender_id: int = Field(foreign_key='user.id')
    sender: 'User' = Relationship(
        sa_relationship_kwargs={
            'foreign_keys': 'Friend.sender_id',
        },
        back_populates='friends_sent',
    )

    recipient_id: int = Field(foreign_key='user.id')
    recipient: 'User' = Relationship(
        sa_relationship_kwargs={
            'foreign_keys': 'Friend.recipient_id',
        },
        back_populates='friends_received',
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
