from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.friendship import schemas
from src.friendship.exceptions import (
    CannotAcceptFriendshipRequest,
    CannotCancelFriendshipRequest,
    CannotCreateFriendshipRequest,
    CannotRejectFriendshipRequest,
)
from src.friendship.models import FriendshipRequest


if TYPE_CHECKING:
    from pydantic import PositiveInt
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_friends(
    account_id: PositiveInt,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> schemas.Friends:

    account = await Account.get(session, account_id)
    friends = await account.get_friends(session)

    friends_response = []
    for friend in friends:
        friends_response.append(
            schemas.Friend(
                account=schemas.FriendAccount.model_validate(friend.Account, from_attributes=True),
                profile=schemas.FriendProfile.model_validate(friend.Profile, from_attributes=True),
                friendship=schemas.FriendFriendship.model_validate(friend.Friendship, from_attributes=True),
            ),
        )

    return schemas.Friends(friends=friends_response)


async def create_friendship_request(
    new_friendship_request: schemas.NewFriendshipRequest,
    current_account: Account,
    session: AsyncSession,
) -> schemas.FriendshipRequest:
    if new_friendship_request.sender_id != current_account.id:
        raise CannotCreateFriendshipRequest()

    friendship_request = await FriendshipRequest.create(session, new_friendship_request)
    return schemas.FriendshipRequest.model_validate(friendship_request, from_attributes=True)


async def cancel_friendship_request(
    request_id: PositiveInt,
    current_account: Account,
    session: AsyncSession,
) -> None:
    friendship_request = await current_account.get_friendship_request(session, request_id)
    if friendship_request.sender_id != current_account.id:
        raise CannotCancelFriendshipRequest()
    await friendship_request.delete(session)


async def accept_friendship_request(
    request_id: PositiveInt,
    current_account: Account,
    session: AsyncSession,
) -> schemas.Friendships:
    friendship_request = await current_account.get_friendship_request(session, request_id)
    if friendship_request.sender_id != current_account.id:
        raise CannotAcceptFriendshipRequest()
    friendships = await friendship_request.accept(session)
    return schemas.Friendships.model_validate({"friendships": friendships}, from_attributes=True)


async def reject_friendship_request(
    request_id: PositiveInt,
    current_account: Account,
    session: AsyncSession,
) -> schemas.FriendshipRequest:
    friendship_request = await current_account.get_friendship_request(session, request_id)
    if friendship_request.sender_id != current_account.id:
        raise CannotRejectFriendshipRequest()
    await friendship_request.reject(session)
    return schemas.FriendshipRequest.model_validate(friendship_request, from_attributes=True)


async def get_friendship_requests(
    account_id: PositiveInt,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> schemas.FriendshipRequests:
    account = await Account.get(session, account_id)
    friendship_requests = await account.get_friendship_requests(session)
    return schemas.FriendshipRequests.model_validate({"requests": friendship_requests}, from_attributes=True)
