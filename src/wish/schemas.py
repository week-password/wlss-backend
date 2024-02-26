from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import PositiveInt

from src.shared.schemas import Schema


class Wish(Schema):
    id: PositiveInt  # noqa: A003

    account_id: PositiveInt
    avatar_id: UUID | None = None
    created_at: datetime
    description: str
    title: str


class Wishes(Schema):
    wishes: list[Wish]


class NewWish(Schema):
    avatar_id: UUID | None = None
    description: str
    title: str


class WishUpdate(Schema):
    avatar_id: UUID | None = None
    description: str
    title: str


class WishBooking(Schema):
    account_id: PositiveInt
    created_at: datetime
    wish_id: PositiveInt


class WishBookings(Schema):
    wish_bookings: list[WishBooking]


class NewWishBooking(Schema):
    account_id: PositiveInt
    wish_id: PositiveInt
