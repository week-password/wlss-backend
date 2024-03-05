from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Account
from src.auth.dependencies import get_account_from_access_token
from src.shared import swagger as shared_swagger
from src.shared.database import get_session
from src.shared.fields import IdField
from src.wish import controllers
from src.wish.dtos import (
    CreateWishBookingRequest,
    CreateWishBookingResponse,
    CreateWishRequest,
    CreateWishResponse,
    GetAccountWishesResponse,
    GetWishBookingsResponse,
    UpdateWishRequest,
    UpdateWishResponse,
)


router = APIRouter(tags=["wish"])


@router.post(
    "/accounts/{account_id}/wishes",
    description="Create a new wish for an account.",
    responses={
        status.HTTP_201_CREATED: {"description": "New wish is created, wish info is returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_201_CREATED,
    summary="Create a wish.",
)
async def create_wish(
    account_id: Annotated[IdField, Path(example=42)],
    request_data: Annotated[CreateWishRequest, Body()],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> CreateWishResponse:
    return await controllers.create_wish(account_id, request_data, current_account, session)


@router.put(
    "/accounts/{account_id}/wishes/{wish_id}",
    description="Update particular wish info.",
    responses={
        status.HTTP_200_OK: {"description": "Wish info is updated. Wish is returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Update particular wish.",
)
async def update_wish(
    account_id: Annotated[IdField, Path(example=42)],
    wish_id: Annotated[IdField, Path(example=17)],
    request_data: Annotated[UpdateWishRequest, Body()],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> UpdateWishResponse:
    return await controllers.update_wish(account_id, wish_id, request_data, current_account, session)


@router.delete(
    "/accounts/{account_id}/wishes/{wish_id}",
    description="Delete particular wish and related bookings.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Wish and related bookings are deleted."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete particular wish.",
)
async def delete_wish(
    account_id: Annotated[IdField, Path(example=42)],
    wish_id: Annotated[IdField, Path(example=17)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> None:
    return await controllers.delete_wish(account_id, wish_id, current_account, session)


@router.get(
    "/accounts/{account_id}/wishes",
    description="Get wishes owned by particular account",
    responses={
        status.HTTP_200_OK: {"descriprtion": "Wishes owned by particular account are returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Get account wishes.",
)
async def get_account_wishes(
    account_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> GetAccountWishesResponse:
    return await controllers.get_account_wishes(account_id, current_account, session)


@router.post(
    "/accounts/{account_id}/wishes/{wish_id}/bookings",
    description="Book particular wish for particular account.",
    responses={
        status.HTTP_201_CREATED: {"description": "Wish booking is created successfully. Booking info returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_201_CREATED,
    summary="Book particular wish.",
)
async def create_wish_booking(
    account_id: Annotated[IdField, Path(example=42)],
    wish_id: Annotated[IdField, Path(example=18)],
    request_data: Annotated[CreateWishBookingRequest, Body()],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> CreateWishBookingResponse:
    return await controllers.create_wish_booking(account_id, wish_id, request_data, current_account, session)


@router.get(
    "/accounts/{account_id}/wishes/bookings",
    description="Get wish bookings info for particular wishes.",
    responses={
        status.HTTP_200_OK: {"description": "Wish bookings for requested wishes are returned"},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
    },
    status_code=status.HTTP_200_OK,
    summary="Get wish bookings.",
)
async def get_wish_bookings(
    account_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> GetWishBookingsResponse:
    """Get wish bookings for particular wishes."""
    return await controllers.get_wish_bookings(account_id, current_account, session)


@router.delete(
    "/accounts/{account_id}/wishes/{wish_id}/bookings/{booking_id}",
    description="Delete particular wish booking.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Wish Booking has been removed."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete wish booking.",
)
async def delete_wish_booking(
    account_id: Annotated[IdField, Path(example=10)],
    wish_id: Annotated[IdField, Path(example=42)],
    booking_id: Annotated[IdField, Path(example=18)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> None:
    return await controllers.delete_wish_booking(account_id, wish_id, booking_id, current_account, session)
