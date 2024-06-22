from sqlmodel import Session

from app import auth
from app.models import User, Token
from app.services import user_service


def authenticate(db: Session, username: str, password: str) -> User | None:
    """
    Authenticates a user
    :param db: database session
    :param username: username
    :param password: user password
    :return: user if success else None
    """
    # first retrieve user by username
    user = user_service.get_user_by_username(
        db=db,
        username=username,
    )
    if not user:
        # return none if user is not found
        return None

    # second, verify that the password is correct
    if not auth.verify_password(
            plain_password=password,
            hashed_password=user.hashed_password,
    ):
        # return None if password is not correct
        return None

    # all good, return user
    return user


def create_token(subject: int) -> Token:
    """
    Creates a new token with the given subject.
    :param subject: subject of the token.
    :return: token
    """
    return Token(
        access_token=auth.create_access_token(
            subject=subject
        )
    )
