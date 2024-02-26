from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.wish import schemas
from src.wish.exceptions import (
    CannotCreateWishBookingError,
    CannotCreateWishError,
    CannotDeleteWishError,
    CannotGetWishBookingsError,
    CannotGetWishesError,
    CannotUpdateWishError,
)
from src.wish.models import WishBooking


if TYPE_CHECKING:
    from pydantic import PositiveInt
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_wish(
    account_id: PositiveInt,
    new_wish: schemas.NewWish,
    current_account: Account,
    session: AsyncSession,
) -> schemas.Wish:
    if account_id != current_account.id:
        raise CannotCreateWishError()
    wish = await current_account.create_wish(session, new_wish)
    return schemas.Wish.model_validate(wish, from_attributes=True)


async def update_wish(
    account_id: PositiveInt,
    wish_id: PositiveInt,
    wish_update: schemas.WishUpdate,
    current_account: Account,
    session: AsyncSession,
) -> schemas.Wish:
    if account_id != current_account.id:
        raise CannotUpdateWishError()
    wish = await current_account.get_wish(session, wish_id)
    await wish.update(session, wish_update)
    return schemas.Wish.model_validate(wish, from_attributes=True)


async def delete_wish(
    account_id: PositiveInt,
    wish_id: PositiveInt,
    current_account: Account,
    session: AsyncSession,
) -> None:
    if account_id != current_account.id:
        raise CannotDeleteWishError()
    wish = await current_account.get_wish(session, wish_id)
    await wish.delete(session)


async def get_account_wishes(
    account_id: PositiveInt,
    current_account: Account,
    session: AsyncSession,
) -> schemas.Wishes:
    account = await Account.get(session, account_id)
    if not (
        account_id == current_account.id
        or await account.has_friend(session, current_account.id)
    ):
        raise CannotGetWishesError()
    wishes = await account.get_wishes(session)
    return schemas.Wishes.model_validate({"wishes": wishes}, from_attributes=True)


async def create_wish_booking(
    account_id: PositiveInt,
    new_wish_booking: schemas.NewWishBooking,
    current_account: Account,
    session: AsyncSession,
) -> schemas.WishBooking:
    account = await Account.get(session, account_id)
    if (
        account_id == current_account.id
        or current_account.id != new_wish_booking.account_id
        or not await account.has_friend(session, current_account.id)
    ):
        raise CannotCreateWishBookingError()
    wish = await account.get_wish(session, new_wish_booking.wish_id)
    wish_booking = await wish.create_booking(session, new_wish_booking.account_id)
    return schemas.WishBooking.model_validate(wish_booking, from_attributes=True)


async def get_wish_bookings(
    account_id: PositiveInt,
    wish_ids: list[PositiveInt],
    current_account: Account,
    session: AsyncSession,
) -> schemas.WishBookings:
    if account_id == current_account.id:
        raise CannotGetWishBookingsError()
    wish_bookings = await WishBooking.find_by_wish_ids(session, wish_ids)
    return schemas.WishBookings.model_validate({"wish_bookings": wish_bookings}, from_attributes=True)


async def delete_wish_booking(
    booking_id: PositiveInt,
    current_account: Account,
    session: AsyncSession,
) -> None:
    wish_booking = await current_account.get_wish_booking(session, booking_id)
    await wish_booking.delete(session)
