from __future__ import annotations

from api.shared.fields import IdField, UuidField
from api.shared.schemas import Schema
from api.wish.fields import WishDescriptionField, WishTitleField


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
