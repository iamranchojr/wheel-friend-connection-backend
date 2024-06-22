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


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Authenticates a user
    :param db: database session
    :param email: user email
    :param password: user password
    :return: user if success else None
    """
    # first retrieve user by email
    user = get_user_by_email(db=db, email=email)
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
