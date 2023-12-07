"""Friendship related endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from pydantic import PositiveInt

from src.auth.dependencies import get_access_token
from src.auth.schemas import AccessTokenPayload
from src.friendship import schemas
from src.shared import swagger as shared_swagger


router = APIRouter(tags=["friendship"])


@router.get(
    "/accounts/{account_id}/friends",
    description="Get profile info of friends of particular account",
    responses={
        status.HTTP_200_OK: {
            "description": "Profile info for account friends is returned.",
            "content": {
                "application/json": {
                    "example": {
                        "friends": [
                            {
                                "account": {
                                    "id": 42,
                                },
                                "friendship": {
                                    "created_at": "2023-06-17T11:47:02.823Z",
                                },
                                "profile": {
                                    "name": "John Doe",
                                    "description": "Who da heck is John Doe?",
                                    "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
                                },
                            },
                            {
                                "account": {
                                    "id": 18,
                                },
                                "friendship": {
                                    "created_at": "2023-08-07T00:18:21.823Z",
                                },
                                "profile": {
                                    "name": "Alan Fresco",
                                    "description": "Who da heck is Alan Fresco?",
                                    "avatar_id": "595f1db3-cdc6-4ef7-bbb4-33c4cedfe172",
                                },
                            },
                        ],
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Friends,
    status_code=status.HTTP_200_OK,
    summary="Get friends.",
)
async def get_friends(
    account_id: Annotated[PositiveInt, Path(example=15)],  # noqa: ARG001
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Get all Account friends."""


@router.post(
    "/friendship/requests",
    description="Create new friendship request.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "New friendship request is created and returned.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 11,
                        "receiver_id": 42,
                        "sender_id": 18,
                        "status": "PENDING",
                        "created_at": "2023-06-17T11:47:02.823Z",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
    },
    response_model=schemas.FriendshipRequest,
    status_code=status.HTTP_201_CREATED,
    summary="Create friendship request.",
)
async def create_friendship_request(
    new_friendship_request: Annotated[  # noqa: ARG001
        schemas.NewFriendshipRequest,
        Body(example={"account_id": 42, "friend_id": 18}),
    ],
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Create new friendship request."""


@router.delete(
    "/friendship/requests/{request_id}",
    description="Cancel (same as delete) existing friendship request.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Friendship request has been removed (same as cancelled).",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel friendship request.",
)
async def cancel_friendship_request(
    request_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Cancel friendship request."""


@router.put(
    "/friendship/requests/{request_id}/accepted",
    description="Accept friendship request and create two friendship relations between two accounts.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Friendship request accepted. New friendship relations returned.",
            "content": {
                "application/json": {
                    "example": {
                        "friendships": [
                            {
                                "account_id": 42,
                                "friend": 18,
                            },
                            {
                                "account_id": 18,
                                "friend": 42,
                            },
                        ],
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Friendships,
    status_code=status.HTTP_201_CREATED,
    summary="Accept friendship request.",
)
async def accept_friendship_request(
    request_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Accept friendship request."""


@router.put(
    "/friendship/requests/{request_id}/rejected",
    description="Reject friendship request.",
    responses={
        status.HTTP_200_OK: {
            "description": "Friendship request is rejected. Updated friendship request info returned.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 7,
                        "receiver_id": 42,
                        "sender_id": 18,
                        "status": "REJECTED",
                        "created_at": "2023-06-17T11:47:02.823Z",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.FriendshipRequest,
    status_code=status.HTTP_200_OK,
    summary="Reject friendship request.",
)
async def reject_friendship_request() -> None:
    """Reject friendship request."""


@router.get(
    "/accounts/{account_id}/friendship/requests",
    description="Get friendship requests related to particular account",
    responses={
        status.HTTP_200_OK: {
            "description": (
                "List of friendship requests is returned. "
                "Requested account may be either in 'receiver_id' or in 'sender_id' field."
            ),
            "content": {
                "application/json": {
                    "example": {
                        "requests": [
                            {
                                "id": 7,
                                "receiver_id": 42,
                                "sender_id": 18,
                                "status": "PENDING",
                                "created_at": "2023-06-17T11:47:02.823Z",
                            },
                            {
                                "id": 21,
                                "receiver_id": 10,
                                "sender_id": 20,
                                "status": "CANCELED",
                                "created_at": "2022-01-08T11:47:02.823Z",
                            },
                            {
                                "id": 53,
                                "receiver_id": 6,
                                "sender_id": 14,
                                "status": "ACCEPTED",
                                "created_at": "2023-03-18T11:47:02.823Z",
                            },
                        ],
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.FriendshipRequests,
    status_code=status.HTTP_200_OK,
    summary="Get friendship requests.",
)
async def get_friendship_requests(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Get all friendship requests related to particular account."""
