from collections.abc import Generator
from typing import Annotated, Type

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from .database import engine
from .models import User, TokenPayload

from . import auth


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/access-token')


def get_db() -> Generator[Session, None, None]:
    """
    Creates an instance of the db session and yields the session object.
    :return: a generator yielding the session object.
    """
    with Session(engine) as session:
        yield session


DatabaseDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(db: DatabaseDep, token: TokenDep) -> Type[User]:
    """
    Gets and returns the current user using the authorization token provided
    :param db: database session
    :param token: authorization token
    :return: the current user
    """
    try:
        # decode access token
        payload = auth.decode_access_token(
            token=token,
        )

        # create token payload with decoded data
        token_data = TokenPayload(**payload)

        # retrieve user from db using the sub
        user = db.get(User, token_data.sub)

        if not user:
            # raise a not found exception if the user was not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found',
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is inactive',
            )

        return user
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
        )


CurrentUserDep = Annotated[User, Depends(get_current_user)]
