from typing import Sequence

from fastapi import APIRouter, status, HTTPException, Query

from app.deps import DatabaseDep, CurrentUserDep
from app.models import FriendRequest, FriendPublic, FriendBase, FriendStatus, Friend
from app.services import friend_service, user_service


router = APIRouter(
    prefix='/friends',
    tags=['friends'],
)


@router.post(
    path='/request',
    description='This endpoint sends a friend request to another user',
    status_code=status.HTTP_201_CREATED,
    response_model=FriendPublic,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Self friend request not allowed',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Recipient not found or inactive',
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Conflict',
        }
    }
)
async def request_friend(
        db: DatabaseDep,
        current_user: CurrentUserDep,  # user needs to be authenticated
        data: FriendRequest
) -> FriendBase:
    # validate that the recipient id provided indeed belongs to a user
    recipient_user = user_service.get_user_by_id(db=db, user_id=data.recipient_id)

    if not recipient_user or not recipient_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Recipient not found or inactive',
        )

    # make sure user is not trying to send a request to themselves
    if recipient_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You cannot send a friend request to yourself',
        )

    friend = friend_service.create_friend(
        db=db,
        current_user=current_user,
        data=data,
    )

    if not friend:
        # friend already exists
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='You already have an existing friendship with this user.',
        )

    # created successfully

    # TODO: send email/notification to recipient

    return friend


_accept_decline_friend_responses = {
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Friend request not pending or current user is not recipient',
    },
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Unauthorized',
    },
    status.HTTP_403_FORBIDDEN: {
        'description': 'Credentials validation failed',
    },
    status.HTTP_404_NOT_FOUND: {
        'description': 'Friend record not found',
    },
}


@router.put(
    path='/{friend_id}/accept',
    name='Accept Friend Request',
    description='This endpoint accepts a pending friend request from another user.',
    status_code=status.HTTP_201_CREATED,
    response_model=FriendPublic,
    responses=_accept_decline_friend_responses
)
async def accept_friend(
        db: DatabaseDep,
        friend_id: int,
        current_user: CurrentUserDep,  # user needs to be authenticated
) -> FriendBase:
    # get friend record with id
    friend = friend_service.get_friend_by_id(
        db=db,
        friend_id=friend_id,
    )

    if not friend:
        # raise exception if friend is None
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No friend record was found',
        )

    # validate that friend is pending
    if friend.status != FriendStatus.Pending or friend.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This friend request cannot be accepted',
        )

    # all good
    friend = friend_service.accept_friend(
        db=db,
        friend=friend,
    )

    # TODO: send email/notification to recipient

    return friend


@router.put(
    path='/{friend_id}/decline',
    name='Decline Friend Request',
    description='This endpoint declines a pending friend request from another user.',
    status_code=status.HTTP_201_CREATED,
    response_model=FriendPublic,
    responses=_accept_decline_friend_responses
)
async def decline_friend(
        db: DatabaseDep,
        friend_id: int,
        current_user: CurrentUserDep,  # user needs to be authenticated
) -> FriendBase:
    # get friend record with id
    friend = friend_service.get_friend_by_id(
        db=db,
        friend_id=friend_id,
    )

    if not friend:
        # raise exception if friend is None
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No friend record was found',
        )

    # validate that friend is pending
    if friend.status != FriendStatus.Pending or friend.recipient_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This friend request cannot be accepted',
        )

    # all good
    friend = friend_service.decline_friend(
        db=db,
        friend=friend,
    )

    # TODO: send email/notification to recipient

    return friend


@router.get(
    path='/list',
    name='Get Current User Friends',
    description='This endpoint returns all current user friends. '
                'It only only returns those pending or accepted',
    response_model=list[FriendPublic],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
    }
)
async def get_friends(
        db: DatabaseDep,
        current_user: CurrentUserDep,

        # using seek based pagination as it offers more performance benefits compared to offset
        seek_id: int = Query(
            0,
            description='This value should be the last id of the most recent data that was fetched'
        ),
        limit: int = 50,
) -> Sequence[Friend]:
    friends = friend_service.get_user_friends(
        db=db,
        user=current_user,
        seek_id=seek_id,
        limit=limit,
    )

    return friends


@router.get(
    path='/get-with-other-user',
    name='Get Friend With Other User',
    description='This endpoint returns a friend record between current user and other user.',
    response_model=FriendPublic,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Unauthorized',
        },
        status.HTTP_403_FORBIDDEN: {
            'description': 'Credentials validation failed',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'No record found',
        },
    }
)
async def get_friend_with_other_user(
        db: DatabaseDep,
        current_user: CurrentUserDep,
        other_user_id: int = Query(
            0,
            description='id of the other user'
        ),
) -> Friend:
    friend = friend_service.get_friend_between_users(
        db=db,
        user_a_id=current_user.id,
        user_b_id=other_user_id,
    )

    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No friend record was found',
        )

    return friend
