from datetime import datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.config import settings

password_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
)


_ALGORITHM = 'HS256'


def create_access_token(subject: int) -> str:
    """
    Create a JWT access token using the given subject and expires_delta.
    :param subject: The subject of the JWT.
    :return: The JWT access token.
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        'exp': expire,
        'sub': str(subject),
    }
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=_ALGORITHM,
    )

    return encoded_jwt


def decode_access_token(token: str) -> Any:
    """
    Decode a JWT access token.
    :param token: The JWT access token.
    :return: The decoded JWT.
    """
    return jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,
        algorithms=[_ALGORITHM],
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the given plain_password matches the given hashed_password.
    :param plain_password: The plaintext password.
    :param hashed_password: The hashed password.
    :return: True if the given plain_password matches the given hashed_password else False.
    """
    return password_context.verify(
        secret=plain_password,
        hash=hashed_password,
    )


def get_password_hash(password: str) -> str:
    """
    Hashes the given password.
    :param password: The password.
    :return: The hashed password.
    """
    return password_context.hash(password)
