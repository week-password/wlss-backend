"""Wish related endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import PositiveInt

from src.auth.security import get_token
from src.shared import swagger as shared_swagger
from src.wish import schemas


router = APIRouter(tags=["wish"])


@router.post(
    "/accounts/{account_id}/wishes",
    description="Create a new wish for an account.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "New wish is created, wish info is returned.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 17,
                        "account_id": 42,
                        "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
                        "title": "Horse",
                        "description": "I'm gonna take my horse to the old town road.",
                        "created_at": "2023-06-17T11:47:02.823Z",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Wish,
    status_code=status.HTTP_201_CREATED,
    summary="Create a wish.",
)
async def create_wish(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    new_wish: Annotated[  # noqa: ARG001
        schemas.NewWish,
        Body(
            example={
                "title": "Horse",
                "description": "I'm gonna take my horse to the old town road.",
                "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
            },
        ),
    ],
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Create a wish."""


@router.put(
    "/accounts/{account_id}/wishes/{wish_id}",
    description="Update particular wish info.",
    responses={
        status.HTTP_200_OK: {
            "description": "Wish info is updated. Wish is returned.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 17,
                        "account_id": 42,
                        "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
                        "title": "Horse",
                        "description": "I'm gonna take my horse to the old town road.",
                        "created_at": "2023-06-17T11:47:02.823Z",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Wish,
    status_code=status.HTTP_200_OK,
    summary="Update particular wish.",
)
async def update_wish(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    wish_id: Annotated[PositiveInt, Path(example=17)],  # noqa: ARG001
    wish_update: Annotated[  # noqa: ARG001
        schemas.WishUpdate,
        Body(
            example={
                "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
                "title": "Horse",
                "description": "I'm gonna take my horse to the old town road.",
            },
        ),
    ],
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Update wish info."""


@router.delete(
    "/accounts/{account_id}/wishes/{wish_id}",
    description="Delete particular wish and related bookings.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Wish and related bookings are deleted.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete particular wish.",
)
async def delete_wish(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    wish_id: Annotated[PositiveInt, Path(example=17)],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Delete wish."""


@router.get(
    "/accounts/{account_id}/wishes",
    description="Get wishes owned by particular account",
    responses={
        status.HTTP_200_OK: {
            "descriprtion": "Wishes owned by particular account are returned.",
            "content": {
                "application/json": {
                    "example": {
                        "wishes": [
                            {
                                "id": 17,
                                "account_id": 42,
                                "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
                                "title": "Horse",
                                "description": "I'm gonna take my horse to the old town road.",
                                "created_at": "2023-06-17T11:47:02.823Z",
                            },
                            {
                                "id": 21,
                                "account_id": 42,
                                "avatar": "/files/92f97bc4-c3d3-4980-86c8-0131c1bedffc",
                                "title": "Sleep",
                                "description": "I need some sleep. Time to put the old horse down.",
                                "created_at": "2023-10-11T18:31:42.715Z",
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
    response_model=schemas.Wishes,
    status_code=status.HTTP_200_OK,
    summary="Get account wishes.",
)
async def get_account_wishes(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get wishes owned by particular account."""


@router.post(
    "/accounts/{account_id}/wishes/{wish_id}/bookings",
    description="Book particular wish for particular account.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Wish booking is created successfully. Booking info returned.",
            "content": {
                "application/json": {
                    "example": {
                        "account_id": 42,
                        "wish_id": 17,
                        "created_at": "2023-06-17T11:47:02.823Z",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.WishBooking,
    status_code=status.HTTP_201_CREATED,
    summary="Book particular wish.",
)
async def create_wish_booking(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    new_wish_booking: Annotated[  # noqa: ARG001
        schemas.NewWishBooking,
        Body(
            example={
                "account_id": 42,
                "wish_id": 17,
            },
        ),
    ],
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Create wish booking."""


@router.get(
    "/bookings",
    description="Get wish bookings info for particular wishes.",
    responses={
        status.HTTP_200_OK: {
            "description": "Wish bookings for requested wishes are returned",
            "content": {
                "application/json": {
                    "example": {
                        "bookings": [
                            {
                                "account_id": 17,
                                "created_at": "2023-10-11T18:31:42.715Z",
                                "wish_id": 42,
                            },
                            {
                                "account_id": 21,
                                "created_at": "2023-06-17T11:47:02.823Z",
                                "wish_id": 18,
                            },
                        ],
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
    },
    status_code=status.HTTP_200_OK,
    response_model=schemas.WishBookings,
    summary="Get wish bookings.",
)
def get_wish_bookings(
    wish_ids: Annotated[list[PositiveInt], Query(example=[42, 18], alias="wish_id")],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get wish bookings for particular wishes."""


@router.delete(
    "/bookings/{booking_id}",
    description="Delete particular wish booking.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Wish Booking has been removed.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete wish booking.",
)
async def delete_wish_booking(
    booking_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Delete wish booking."""
