from __future__ import annotations

from pydantic import Field

from src.friendship.enums import FriendshipRequestStatus
from src.profile.fields import ProfileDescriptionField, ProfileNameField
from src.shared.fields import IdField, UtcDatetimeField, UuidField
from src.shared.schemas import Schema


class GetFriendsResponse(Schema):
    friends: list[_Friend]
    class _Friend(Schema):  # noqa: E301

        account: _FriendAccount
        class _FriendAccount(Schema):  # noqa: E301
            id: IdField = Field(..., example=42)  # noqa: A003

        friendship: _FriendFriendship
        class _FriendFriendship(Schema):  # noqa: E301
            created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")

        profile: _FriendProfile
        class _FriendProfile(Schema):  # noqa: E301
            account_id: IdField = Field(..., example=42)
            avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
            description: ProfileDescriptionField | None = Field(..., example="Who da heck is John Doe?")
            name: ProfileNameField = Field(..., example="John Doe")


class CreateFriendshipRequestRequest(Schema):
    receiver_id: IdField = Field(..., example=42)
    sender_id: IdField = Field(..., example=18)


class CreateFriendshipRequestResponse(Schema):
    id: IdField = Field(..., example=11)  # noqa: A003
    created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
    receiver_id: IdField = Field(..., example=18)
    sender_id: IdField = Field(..., example=42)
    status: FriendshipRequestStatus = Field(..., example="PENDING")


class AcceptFriendshipRequestResponse(Schema):
    friendships: list[_Friendship]
    class _Friendship(Schema):  # noqa: E301
        account_id: IdField = Field(..., example=42)
        created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
        friend_id: IdField = Field(..., example=18)


class RejectFriendshipRequestResponse(Schema):
    id: IdField = Field(..., example=7)  # noqa: A003
    created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
    receiver_id: IdField = Field(..., example=42)
    sender_id: IdField = Field(..., example=18)
    status: FriendshipRequestStatus = Field(..., example="REJECTED")


class GetFriendshipRequestsResponse(Schema):
    requests: list[_FriendshipRequest]
    class _FriendshipRequest(Schema):  # noqa: E301
        id: IdField = Field(..., example=7)  # noqa: A003
        created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
        receiver_id: IdField = Field(..., example=42)
        sender_id: IdField = Field(..., example=18)
        status: FriendshipRequestStatus = Field(..., example="PENDING")
