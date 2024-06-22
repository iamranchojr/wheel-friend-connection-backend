from sqlmodel import Session, select

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
