from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app import auth
from app.deps import DatabaseDep
from app.models import AuthResponse, Token, AuthResponseOut
from app.models.user_model import UserRegister
from app.services import user_service

router = APIRouter()


@router.post(
    path='/register',
    status_code=status.HTTP_201_CREATED,
    response_model=AuthResponseOut,
)
def register_user(db: DatabaseDep, data: UserRegister) -> AuthResponse:
    """
    Register a new user.
    :param db: database session
    :param data: user register data
    """

    # begin by validating email to make sure it can be used
    user = user_service.get_user_by_email(
        db=db,
        email=data.email,
    )
    if user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Email already registered',
        )

    # all good, validate and create user
    data = UserRegister.model_validate(data)
    user = user_service.create_user(
        db=db,
        data=data,
    )

    # create access token for user
    token = Token(
        access_token=auth.create_access_token(
            subject=user.id
        )
    )

    # return access token and user
    return AuthResponse(
        token=token,
        user=user,
    )
