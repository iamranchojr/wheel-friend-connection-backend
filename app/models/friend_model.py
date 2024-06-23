from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    # to get around circular imports
    from .user_model import User, UserPublic


class FriendStatus(str, Enum):
    Pending: str = 'Pending'
    Accepted: str = 'Accepted'
    Declined: str = 'Declined'


class FriendBase(SQLModel):
    status: FriendStatus = Field(default=FriendStatus.Pending.value)
    message: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Friend(FriendBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    sender_id: int = Field(foreign_key='user.id')
    sender: 'User' = Relationship(
        sa_relationship_kwargs={
            'foreign_keys': 'Friend.sender_id',
            'lazy': 'joined',  # eager load the data
        },
        back_populates='friends_sent',
    )

    recipient_id: int = Field(foreign_key='user.id')
    recipient: 'User' = Relationship(
        sa_relationship_kwargs={
            'foreign_keys': 'Friend.recipient_id',
            'lazy': 'joined',  # eager load the data
        },
        back_populates='friends_received',
    )


class FriendRequest(SQLModel):
    recipient_id: int
    message: str | None = None
