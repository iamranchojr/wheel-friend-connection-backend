from datetime import datetime
from typing import Sequence

from sqlmodel import Session, select, col

from app import auth
from app.models.user_model import UserRegister, User


def create_user(db: Session, data: UserRegister) -> User:
    """
    Creates a new user
    :param db: database session
    :param data: user data
    :return: created user
    """
    # create user instance
    user = User.model_validate(
        data,
        update={
            'username': data.email,
            'hashed_password': auth.get_password_hash(
                password=data.password,
            )
        }
    )

    # add to db and commit
    db.add(user)
    db.commit()

    # refresh user from db and return it
    db.refresh(user)
    return user


def update_user_bio(
        db: Session,
        user: User,
        bio: str,
) -> User:
    """
    Updates the bio of a user
    :param db: database session
    :param user: user to update
    :param bio: new bio
    :return: updated user
    """
    # update user bio
    user.bio = bio
    user.updated_at = datetime.utcnow()

    # add to db and commit changes
    db.add(user)
    db.commit()

    # refresh and return user
    db.refresh(user)
    return user


def update_user_status(
        db: Session,
        user: User,
        status: str,
) -> User:
    """
    Updates the status of a user
    :param db: database session
    :param user: user to update
    :param status: user status
    :return: updated user
    """
    # update user status
    user.status = status
    user.updated_at = datetime.utcnow()

    # add to db and commit changes
    db.add(user)
    db.commit()

    # refresh and return user
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Gets a user by their id
    :param db: database session
    :param user_id: user id
    :return: user if found else None
    """
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Gets a user by email
    :param db: database session
    :param email: user email
    :return: user if found else None
    """
    query = select(User).where(User.email == email)
    user = db.exec(query).first()
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Gets a user by username
    :param db: database session
    :param username: user username
    :return: user if found else None
    """
    query = select(User).where(User.username == username)
    user = db.exec(query).first()
    return user


def get_active_users(
        db: Session,
        query: str = None,
        seek_id: int = 0,
        limit: int = 50,
) -> Sequence[User]:
    """
    Gets all active users
    :param db: database session
    :param query: query to filter
    :param seek_id: seek id
    :param limit: limit
    """
    statement = (select(User).where(
        User.is_active == True,

        # using seek based pagination as it offers more performance benefits compared to offset
        User.id > seek_id,
    ))

    if query:
        # case-insensitive match
        statement = statement.where(col(User.name).regexp_match(query, 'i'))

    # paginate and return
    statement = statement.limit(limit)
    return db.exec(statement).all()
