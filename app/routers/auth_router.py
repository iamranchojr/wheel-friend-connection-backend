from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.deps import DatabaseDep
from app.models import AuthResponseOut, AuthResponse, Token
from app.services import auth_service


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post(
    path='/login',
    name='Login user',
    response_model=AuthResponseOut,
    description='Login user. This endpoint will return both the token and user data',
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Invalid credentials',
        }
    }
)
async def login(
        db: DatabaseDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AuthResponse:
    # authenticate user
    user = auth_service.authenticate(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )

    if not user:
        # username or password is incorrect, raise bad request exception
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password',
        )

    # return access token and user
    return AuthResponse(
        token=auth_service.create_token(subject=user.id),
        user=user,
    )


@router.post(
    path='/access-token',
    name='Get access token',
    description='Retrieve access token. This endpoint will return only the access token',
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Invalid credentials',
        }
    }
)
async def access_token(
        db: DatabaseDep,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # authenticate user
    user = auth_service.authenticate(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )

    if not user:
        # username or password is incorrect, raise bad request exception
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password',
        )

    # return access token and user
    return auth_service.create_token(subject=user.id)
