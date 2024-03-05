from __future__ import annotations

from pydantic import Field

from src.friendship.enums import FriendshipRequestStatus
from src.shared.fields import IdField, UtcDatetimeField
from src.shared.schemas import Schema


class GetAccountFriendshipsResponse(Schema):
    friendships: list[_Friendship]
    class _Friendship(Schema):  # noqa: E301
        account_id: IdField = Field(..., example=42)
        created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
        friend_id: IdField = Field(..., example=18)


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
