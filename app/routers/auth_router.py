from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.deps import DatabaseDep
from app.models import AuthResponseOut, AuthResponse
from app.services import auth_service


router = APIRouter(
    prefix='/auth',
    tags=['users'],
)


@router.post(
    path='/access-token',
    response_model=AuthResponseOut,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Invalid credentials',
        }
    }
)
async def authenticate(
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
