from __future__ import annotations

from src.shared.fields import IdField, UtcDatetimeField, UuidField
from src.shared.schemas import Schema
from src.wish.fields import WishDescriptionField, WishTitleField


class Wish(Schema):
    id: IdField  # noqa: A003

    account_id: IdField
    avatar_id: UuidField | None = None
    created_at: UtcDatetimeField
    description: WishDescriptionField
    title: WishTitleField


class Wishes(Schema):
    wishes: list[Wish]


class NewWish(Schema):
    avatar_id: UuidField | None = None
    description: WishDescriptionField
    title: WishTitleField


class WishUpdate(Schema):
    avatar_id: UuidField | None = None
    description: WishDescriptionField
    title: WishTitleField


class WishBooking(Schema):
    account_id: IdField
    created_at: UtcDatetimeField
    wish_id: IdField


class WishBookings(Schema):
    wish_bookings: list[WishBooking]


class NewWishBooking(Schema):
    account_id: IdField
    wish_id: IdField
