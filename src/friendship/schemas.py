from __future__ import annotations

from uuid import UUID

from src.friendship.enums import FriendshipRequestStatus
from src.profile.fields import ProfileDescriptionField, ProfileNameField
from src.shared.fields import IdField, UtcDatetimeField
from src.shared.schemas import Schema


class NewFriendship(Schema):
    account_id: IdField
    friend_id: IdField


class Friendship(Schema):
    account_id: IdField
    created_at: UtcDatetimeField
    friend_id: IdField


class Friendships(Schema):
    friendships: list[Friendship]


class FriendshipRequest(Schema):
    id: IdField  # noqa: A003

    created_at: UtcDatetimeField
    receiver_id: IdField
    sender_id: IdField
    status: FriendshipRequestStatus


class FriendshipRequests(Schema):
    requests: list[FriendshipRequest]


class NewFriendshipRequest(Schema):
    receiver_id: IdField
    sender_id: IdField


class Friend(Schema):
    account: FriendAccount
    profile: FriendProfile
    friendship: FriendFriendship


class FriendAccount(Schema):
    id: IdField  # noqa: A003


class FriendProfile(Schema):
    account_id: IdField
    avatar_id: UUID | None = None
    description: ProfileDescriptionField | None
    name: ProfileNameField


class FriendFriendship(Schema):
    created_at: UtcDatetimeField


class Friends(Schema):
    friends: list[Friend]
