from sqlmodel import SQLModel

from .token_model import Token
from .user_model import UserBase, CurrentUser


class AuthResponse(SQLModel):
    token: Token
    user: UserBase


class AuthResponseOut(AuthResponse):
    user: CurrentUser

