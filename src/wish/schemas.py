"""Schemas for wish related functionality."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import PositiveInt

from src.shared.schemas import Schema


class Wish(Schema):
    """Existing wish model."""

    id: PositiveInt  # noqa: A003

    account_id: PositiveInt
    avatar_id: UUID | None = None
    created_at: datetime
    description: str
    title: str


class Wishes(Schema):
    """Multiple wishes."""

    wishes: list[Wish]


class NewWish(Schema):
    """Wish which is going to be created."""

    avatar_id: UUID | None = None
    description: str
    title: str


class WishUpdate(Schema):
    """Update info for wish."""

    avatar_id: UUID | None = None
    description: str
    title: str


class WishBooking(Schema):
    """Existing wish booking."""

    account_id: PositiveInt
    created_at: datetime
    wish_id: PositiveInt


class WishBookings(Schema):
    """Multiple wish bookings."""

    wish_bookings: list[WishBooking]


class NewWishBooking(Schema):
    """Wish booking which is going to be created."""

    account_id: PositiveInt
    wish_id: PositiveInt
