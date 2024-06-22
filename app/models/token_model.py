from enum import Enum

from sqlmodel import SQLModel


class TokenType(str, Enum):
    """
    Enum defining various token types
    """
    Bearer = 'bearer'


class Token(SQLModel):
    """
    JSON payload containing access token
    """
    access_token: str
    token_type: TokenType = TokenType.Bearer


class TokenPayload(SQLModel):
    """
    Token payload which contains the subject
    """
    sub: int | None = None
