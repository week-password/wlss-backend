from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import PositiveInt

from src.friendship.enums import FriendshipRequestStatus
from src.shared.schemas import Schema


class NewFriendship(Schema):
    account_id: PositiveInt
    friend_id: PositiveInt


class Friendship(Schema):
    account_id: PositiveInt
    created_at: datetime
    friend_id: PositiveInt


class Friendships(Schema):
    friendships: list[Friendship]


class FriendshipRequest(Schema):
    id: PositiveInt  # noqa: A003

    created_at: datetime
    receiver_id: PositiveInt
    sender_id: PositiveInt
    status: FriendshipRequestStatus


class FriendshipRequests(Schema):
    requests: list[FriendshipRequest]


class NewFriendshipRequest(Schema):
    receiver_id: PositiveInt
    sender_id: PositiveInt


class Friend(Schema):
    account: FriendAccount
    profile: FriendProfile
    friendship: FriendFriendship


class FriendAccount(Schema):
    id: PositiveInt  # noqa: A003


class FriendProfile(Schema):
    account_id: PositiveInt
    avatar_id: UUID | None = None
    description: str | None
    name: str


class FriendFriendship(Schema):
    created_at: datetime


class Friends(Schema):
    friends: list[Friend]
