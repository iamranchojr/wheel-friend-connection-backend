from datetime import datetime
from typing import Sequence

from sqlmodel import Session, select, or_

from app.models import FriendRequest, Friend, User, FriendStatus


def _validate_friend_conflict(
        db: Session,
        current_user_id: int,
        recipient_id: int,
) -> bool:
    """
    Validates if a friend object exists between the current user and the recipient
    :param db: database session
    :param current_user_id: current user id
    :param recipient_id: recipient id
    :returns True if no friend object exists else False
    """
    # check if a friend object exists between current user and recipient
    query = select(Friend).where(
        Friend.sender_id == current_user_id,
        Friend.recipient_id == recipient_id,
    )

    friend = db.exec(query).first()
    if friend:
        # friend object already exists
        return False

    # do other way round
    # TODO: research into how to combine this in one query
    query = select(Friend).where(
        Friend.recipient_id == current_user_id,
        Friend.sender_id == recipient_id,
    )

    friend = db.exec(query).first()
    if friend:
        # friend object already exists
        return False

    # no friend exists
    return True


def create_friend(
        db: Session,
        current_user: User,
        data: FriendRequest,
) -> Friend | None:
    """
    Creates a new friend object between current user and the recipient user
    :param db: database session
    :param current_user: current user
    :param data: friend data
    :return: friend object or None if friend object already exists between the two users
    """
    can_create = _validate_friend_conflict(
        db=db,
        current_user_id=current_user.id,
        recipient_id=data.recipient_id,
    )

    if not can_create:
        return None

    # safe to create a new friend object
    friend = Friend(
        sender_id=current_user.id,
        recipient_id=data.recipient_id,
        message=data.message,
        status=FriendStatus.Pending,
    )

    # add to db and commit
    db.add(friend)
    db.commit()

    return friend


def accept_friend(
        friend: Friend,
        db: Session,
) -> Friend | None:
    """
    Updates friend object status to accepted
    :param friend: friend object to update
    :param db: database session
    :return: friend object after update or None if friend
    object is not pending or recipient does not match current user
    """
    # all good, accept friend
    friend.status = FriendStatus.Accepted
    friend.updated_at = datetime.utcnow()

    # add to db session and commit changes
    db.add(friend)
    db.commit()

    # refresh and return friend
    db.refresh(friend)
    return friend


def decline_friend(
        friend: Friend,
        db: Session,
) -> Friend | None:
    """
    Updates friend object status to declined
    :param friend: friend object to decline
    :param db: database session
    :return: friend object after update or None if friend
    object is not pending or recipient does not match current user
    """
    # all good, decline friend
    friend.status = FriendStatus.Declined
    friend.updated_at = datetime.utcnow()

    # add to db session and commit changes
    db.add(friend)
    db.commit()

    # refresh and return friend
    db.refresh(friend)
    return friend


def get_friend_by_recipient_id(
        db: Session,
        recipient_id: int
) -> Friend | None:
    """
    Gets a friend object by the sender id
    :param db: database session
    :param recipient_id: recipient id
    :return: friend if found else None
    """
    query = select(Friend).where(Friend.recipient_id == recipient_id)
    return db.exec(query).first()


def get_friend_by_id(
        db: Session,
        friend_id: int
) -> Friend | None:
    """
    Gets a friend object by primary key id
    :param db: database session
    :param friend_id: friend id
    :return: friend if found else None
    """
    return db.get(Friend, friend_id)


def get_user_friends(
        db: Session,
        user: User,
        seek_id: int = 0,
        limit: int = 50,
) -> Sequence[Friend]:
    """
    Get friend objects belonging to the user provided.
    This function only returns pending and accepted friends
    :param db: database session
    :param user: user
    :param seek_id: seek id
    :param limit: limit size
    :return: sequence of friend objects
    """
    # query only accepted and pending friends
    query = select(Friend).where(
        or_(
            Friend.sender_id == user.id,
            Friend.recipient_id == user.id,
        ),
        or_(
            Friend.status == FriendStatus.Pending,
            Friend.status == FriendStatus.Accepted,
        ),

        # using seek based pagination as it offers more performance benefits compared to offset
        Friend.id > seek_id
    ).limit(limit)

    return db.exec(query).all()
