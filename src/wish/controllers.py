from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.wish.dtos import (
    CreateWishBookingResponse,
    CreateWishResponse,
    GetAccountWishesResponse,
    GetWishBookingsResponse,
    UpdateWishResponse,
)
from src.wish.exceptions import (
    CannotCreateWishBookingError,
    CannotCreateWishError,
    CannotDeleteWishBookingError,
    CannotDeleteWishError,
    CannotGetWishBookingsError,
    CannotGetWishesError,
    CannotUpdateWishError,
)
from src.wish.schemas import NewWish, NewWishBooking, WishUpdate


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.shared.types import Id

    from src.wish.dtos import CreateWishBookingRequest, CreateWishRequest, UpdateWishRequest


async def create_wish(
    account_id: Id,
    request_data: CreateWishRequest,
    current_account: Account,
    session: AsyncSession,
) -> CreateWishResponse:
    if account_id != current_account.id:
        raise CannotCreateWishError()
    new_wish = NewWish.from_(request_data)
    wish = await current_account.create_wish(session, new_wish)
    return CreateWishResponse.model_validate(wish, from_attributes=True)


async def update_wish(
    account_id: Id,
    wish_id: Id,
    request_data: UpdateWishRequest,
    current_account: Account,
    session: AsyncSession,
) -> UpdateWishResponse:
    if account_id != current_account.id:
        raise CannotUpdateWishError()
    wish = await current_account.get_wish(session, wish_id)
    wish_update = WishUpdate.from_(request_data)
    await wish.update(session, wish_update)
    return UpdateWishResponse.model_validate(wish, from_attributes=True)


async def delete_wish(
    account_id: Id,
    wish_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> None:
    if account_id != current_account.id:
        raise CannotDeleteWishError()
    wish = await current_account.get_wish(session, wish_id)
    await wish.delete(session)


async def get_account_wishes(
    account_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> GetAccountWishesResponse:
    account = await Account.get(session, account_id)
    if not (
        account_id == current_account.id
        or await account.has_friend(session, current_account.id)
    ):
        raise CannotGetWishesError()
    wishes = await account.get_wishes(session)
    return GetAccountWishesResponse.model_validate({"wishes": wishes}, from_attributes=True)


async def create_wish_booking(
    account_id: Id,
    wish_id: Id,
    request_data: CreateWishBookingRequest,
    current_account: Account,
    session: AsyncSession,
) -> CreateWishBookingResponse:
    new_wish_booking = NewWishBooking.from_(request_data)
    account = await Account.get(session, account_id)
    if (
        account_id == current_account.id
        or current_account.id != new_wish_booking.account_id
        or not await account.has_friend(session, current_account.id)
    ):
        raise CannotCreateWishBookingError()
    wish = await account.get_wish(session, wish_id)
    wish_booking = await wish.create_booking(session, new_wish_booking)
    return CreateWishBookingResponse.model_validate(wish_booking, from_attributes=True)


async def get_wish_bookings(
    account_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> GetWishBookingsResponse:
    if account_id == current_account.id:
        raise CannotGetWishBookingsError()
    account = await Account.get(session, account_id)
    wish_bookings = await account.get_wish_bookings(session)
    return GetWishBookingsResponse.model_validate({"wish_bookings": wish_bookings}, from_attributes=True)


async def delete_wish_booking(
    account_id: Id,
    wish_id: Id,
    booking_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> None:
    if account_id == current_account.id:
        raise CannotDeleteWishBookingError()
    account = await Account.get(session, account_id)
    wish = await account.get_wish(session, wish_id)
    wish_booking = await wish.get_booking(session, booking_id)
    if wish_booking.account_id != current_account.id:
        raise CannotDeleteWishBookingError()
    await wish_booking.delete(session)
