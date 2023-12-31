"""Schemas for friendship related functionality."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import PositiveInt

from src.friendship.enums import FriendshipRequestStatus
from src.shared.schemas import Schema


class Friendship(Schema):
    """Friendship relations between accounts."""

    account_id: PositiveInt
    created_at: datetime
    friend_id: PositiveInt


class Friendships(Schema):
    """Friendship relations list."""

    friendships: list[Friendship]


class FriendshipRequest(Schema):
    """Friendship request."""

    id: PositiveInt  # noqa: A003

    created_at: datetime
    receiver_id: PositiveInt
    sender_id: PositiveInt
    status: FriendshipRequestStatus


class FriendshipRequests(Schema):
    """List of friendship requests."""

    requests: list[FriendshipRequest]


class NewFriendshipRequest(Schema):
    """New friendship which is going to be created."""

    receiver_id: PositiveInt
    sender_id: PositiveInt


class Friend(Schema):
    """Different information someone's friend."""

    account: FriendAccount
    profile: FriendProfile
    friendship: FriendFriendship


class FriendAccount(Schema):
    """Account info of someone's friend."""

    id: PositiveInt  # noqa: A003


class FriendProfile(Schema):
    """Profile info of someone's friend."""

    avatar_id: UUID | None = None
    description: str
    name: str


class FriendFriendship(Schema):
    """Friendship info of someone's friend."""

    created_at: datetime


class Friends(Schema):
    """List of friend profiles."""

    friends: list[FriendProfile]
