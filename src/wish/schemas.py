from __future__ import annotations

from src.shared.fields import IdField, UuidField
from src.shared.schemas import Schema
from src.wish.fields import WishDescriptionField, WishTitleField


class NewWish(Schema):
    avatar_id: UuidField | None = None
    description: WishDescriptionField
    title: WishTitleField


class WishUpdate(Schema):
    avatar_id: UuidField | None = None
    description: WishDescriptionField
    title: WishTitleField


class NewWishBooking(Schema):
    account_id: IdField
