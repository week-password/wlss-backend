from __future__ import annotations

from typing import TYPE_CHECKING

from api.friendship.dtos import (
    AcceptFriendshipRequestResponse,
    CreateFriendshipRequestResponse,
    GetAccountFriendshipsResponse,
    GetFriendshipRequestsResponse,
    RejectFriendshipRequestResponse,
)
from src.account.models import Account
from src.friendship import schemas
from src.friendship.exceptions import (
    CannotAcceptFriendshipRequest,
    CannotCancelFriendshipRequest,
    CannotCreateFriendshipRequest,
    CannotDeleteFriendship,
    CannotRejectFriendshipRequest,
)
from src.friendship.models import FriendshipRequest


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.shared.types import Id

    from api.friendship.dtos import CreateFriendshipRequestRequest


async def get_account_friendships(
    account_id: Id,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> GetAccountFriendshipsResponse:
    account = await Account.get(session, account_id)
    friendships = await account.get_friendships(session)
    return GetAccountFriendshipsResponse.model_validate({"friendships": friendships}, from_attributes=True)


async def create_friendship_request(
    request_data: CreateFriendshipRequestRequest,
    current_account: Account,
    session: AsyncSession,
) -> CreateFriendshipRequestResponse:
    new_friendship_request = schemas.NewFriendshipRequest.from_(request_data)

    if new_friendship_request.sender_id != current_account.id:
        raise CannotCreateFriendshipRequest()

    friendship_request = await FriendshipRequest.create(session, new_friendship_request)
    return CreateFriendshipRequestResponse.model_validate(friendship_request, from_attributes=True)


async def cancel_friendship_request(
    request_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> None:
    friendship_request = await FriendshipRequest.get(session, request_id)
    if friendship_request.sender_id != current_account.id:
        raise CannotCancelFriendshipRequest()
    await friendship_request.delete(session)


async def accept_friendship_request(
    request_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> AcceptFriendshipRequestResponse:
    friendship_request = await FriendshipRequest.get(session, request_id)
    if friendship_request.sender_id != current_account.id:
        raise CannotAcceptFriendshipRequest()
    friendships = await friendship_request.accept(session)
    return AcceptFriendshipRequestResponse.model_validate({"friendships": friendships}, from_attributes=True)


async def reject_friendship_request(
    request_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> RejectFriendshipRequestResponse:
    friendship_request = await FriendshipRequest.get(session, request_id)
    if friendship_request.sender_id != current_account.id:
        raise CannotRejectFriendshipRequest()
    await friendship_request.reject(session)
    return RejectFriendshipRequestResponse.model_validate(friendship_request, from_attributes=True)


async def get_friendship_requests(
    account_id: Id,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> GetFriendshipRequestsResponse:
    account = await Account.get(session, account_id)
    friendship_requests = await account.get_friendship_requests(session)
    return GetFriendshipRequestsResponse.model_validate({"requests": friendship_requests}, from_attributes=True)


async def delete_friendships(
    account_id: Id,
    friend_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> None:
    if account_id != current_account.id:
        raise CannotDeleteFriendship()
    account = await Account.get(session, account_id)
    await account.delete_friendships(session, friend_id)
