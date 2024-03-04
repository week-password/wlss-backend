from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.friendship.dtos import (
    AcceptFriendshipRequestResponse,
    CreateFriendshipRequestRequest,
    CreateFriendshipRequestResponse,
    GetAccountFriendshipsResponse,
    GetFriendshipRequestsResponse,
    RejectFriendshipRequestResponse,
)
from api.shared.fields import IdField
from src.account.models import Account
from src.auth.dependencies import get_account_from_access_token
from src.friendship import controllers
from src.shared import swagger as shared_swagger
from src.shared.database import get_session


router = APIRouter(tags=["friendship"])


@router.get(
    "/accounts/{account_id}/friendships",
    description="Get profile info of friends of particular account",
    responses={
        status.HTTP_200_OK: {"description": "Profile info for account friends is returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Get friends.",
)
async def get_account_friendships(
    account_id: Annotated[IdField, Path(example=15)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> GetAccountFriendshipsResponse:
    return await controllers.get_account_friendships(account_id, current_account, session)


@router.post(
    "/friendships/requests",
    description="Create new friendship request.",
    responses={
        status.HTTP_201_CREATED: {"description": "New friendship request is created and returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
    },
    status_code=status.HTTP_201_CREATED,
    summary="Create friendship request.",
)
async def create_friendship_request(
    request_data: Annotated[CreateFriendshipRequestRequest, Body()],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> CreateFriendshipRequestResponse:
    return await controllers.create_friendship_request(request_data, current_account, session)


@router.delete(
    "/friendships/requests/{request_id}",
    description="Cancel (same as delete) existing friendship request.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Friendship request has been removed (same as cancelled)."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel friendship request.",
)
async def cancel_friendship_request(
    request_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> None:
    return await controllers.cancel_friendship_request(request_id, current_account, session)


@router.put(
    "/friendships/requests/{request_id}/accepted",
    description="Accept friendship request and create two friendship relations between two accounts.",
    responses={
        status.HTTP_201_CREATED: {"description": "Friendship request accepted. New friendship relations returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_201_CREATED,
    summary="Accept friendship request.",
)
async def accept_friendship_request(
    request_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> AcceptFriendshipRequestResponse:
    return await controllers.accept_friendship_request(request_id, current_account, session)


@router.put(
    "/friendships/requests/{request_id}/rejected",
    description="Reject friendship request.",
    responses={
        status.HTTP_200_OK: {
            "description": "Friendship request is rejected. Updated friendship request info returned.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Reject friendship request.",
)
async def reject_friendship_request(
    request_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> RejectFriendshipRequestResponse:
    return await controllers.reject_friendship_request(request_id, current_account, session)


@router.get(
    "/accounts/{account_id}/friendships/requests",
    description="Get friendship requests related to particular account",
    responses={
        status.HTTP_200_OK: {
            "description": (
                "List of friendship requests is returned. "
                "Requested account may be either in 'receiver_id' or in 'sender_id' field."
            ),
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Get friendship requests.",
)
async def get_friendship_requests(
    account_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> GetFriendshipRequestsResponse:
    return await controllers.get_friendship_requests(account_id, current_account, session)


@router.delete(
    "/accounts/{account_id}/friendships/{friend_id}",
    description="Delete friendhips between account_id and friend_id.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Friendships removed."},
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete friend.",
)
async def delete_friendships(
    account_id: Annotated[IdField, Path(example=42)],
    friend_id: Annotated[IdField, Path(example=18)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> None:
    return await controllers.delete_friendships(account_id, friend_id, current_account, session)
