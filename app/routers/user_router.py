from typing import Sequence, Annotated

from fastapi import APIRouter, HTTPException, status, Query, Body

from app.deps import DatabaseDep, CurrentUserDep
from app.models import AuthResponse, AuthResponseOut, User
from app.models.user_model import UserRegister, UserPublic, UserBase, CurrentUser
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
            status_code=status.HTTP_409_CONFLICT,
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


@router.put(
    path='/me',
    name='Get current user',
    description='This endpoint returns the currently authenticated user.',
    response_model=CurrentUser,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
    }
)
async def get_current_user(
        current_user: CurrentUserDep,
) -> UserBase:
    return current_user


@router.put(
    path='/me/update-bio',
    name='Update current user bio',
    description='This endpoint updates the bio of the current user.',
    response_model=CurrentUser,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
    }
)
async def update_current_user_bio(
        db: DatabaseDep,
        current_user: CurrentUserDep,
        bio: Annotated[str, Body(embed=True)]
) -> UserBase:
    return user_service.update_user_bio(
        db=db,
        user=current_user,
        bio=bio,
    )


@router.put(
    path='/me/update-status',
    name='Update current user status',
    description='This endpoint updates the status of the current user, and broadcasts a '
                'real time notification to user friends that are currently online',
    response_model=CurrentUser,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
    }
)
async def update_current_user_status(
        db: DatabaseDep,
        current_user: CurrentUserDep,
        new_status: Annotated[str, Body(embed=True)]
) -> UserBase:
    user = user_service.update_user_status(
        db=db,
        user=current_user,
        status=new_status,
    )

    # TODO: Ideally we should broadcast the websocket event from the backend
    #  but for the purpose of this task and as a proof of work,
    #  the frontend will handle it by sending a message over the channel

    return user


@router.get(
    path='/list',
    name='Get all users',
    description='This endpoint returns all active users friends.',
    response_model=list[UserPublic],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
    }
)
async def get_users(
        db: DatabaseDep,
        _: CurrentUserDep,
        query: str | None = Query(
            default=None,
            description='Query to search users by name'
        ),

        # using seek based pagination as it offers more performance benefits compared to offset
        seek_id: int = Query(
            0,
            description='This value should be the last id of the most recent data that was fetched'
        ),
        limit: int = 50,
) -> Sequence[UserBase]:
    return user_service.get_active_users(
        db=db,
        query=query,
        seek_id=seek_id,
        limit=limit,
    )


@router.get(
    path='/list-users-who-are-friends-with-current-user',
    name='Get all users who are friends with current user',
    description='This endpoint returns all users who are friends with current user.',
    response_model=list[UserPublic],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
    }
)
async def get_users_who_are_friends_with_user(
        db: DatabaseDep,
        current_user: CurrentUserDep,
        seek_id: int = Query(
            0,
            description='This value should be the last id of the most recent data that was fetched'
        ),
        limit: int = 50,
) -> Sequence[User]:
    return user_service.get_users_who_are_friends_with_user(
        db=db,
        user_id=current_user.id,
        seek_id=seek_id,
        limit=limit,
    )
