from .user_model import User, UserBase, CurrentUser, UserPublic
from .friend_model import FriendBase, Friend, FriendStatus, FriendRequest
from .token_model import Token, TokenPayload, TokenType
from .auth_model import AuthResponse, AuthResponseOut


# this has been placed here to prevent circular imports, at least for now
# https://github.com/tiangolo/fastapi/discussions/11423
class FriendPublic(FriendBase):
    """
    This model is used as the response model for Friend
    to take advantage of fast api's data filtering
    """
    id: int
    sender_id: int
    recipient_id: int
    sender: UserPublic
    recipient: UserPublic
