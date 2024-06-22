from http import HTTPStatus

from fastapi import APIRouter, HTTPException, status

from app.deps import DatabaseDep
from app.models import AuthResponse, AuthResponseOut
from app.models.user_model import UserRegister
from app.services import user_service, auth_service


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post(
    path='/register',
    status_code=status.HTTP_201_CREATED,
    response_model=AuthResponseOut,
    description='Register a new user with provided name, email, and password.',
    responses={
        status.HTTP_409_CONFLICT: {
            'description': 'Email conflict',
        }
    }
)
async def register_user(db: DatabaseDep, data: UserRegister) -> AuthResponse:
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
        # if email not available, raise a conflict exception
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Provided email belongs to another user.',
        )

    # all good, validate and create user
    data = UserRegister.model_validate(data)
    user = user_service.create_user(
        db=db,
        data=data,
    )

    # return access token and user
    return AuthResponse(
        token=auth_service.create_token(subject=user.id),
        user=user,
    )
