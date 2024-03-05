from __future__ import annotations

from pydantic import Field

from src.shared.fields import IdField, UtcDatetimeField, UuidField
from src.shared.schemas import Schema
from src.wish.fields import WishDescriptionField, WishTitleField


class CreateWishRequest(Schema):
    avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
    description: WishDescriptionField = Field(..., example="I'm gonna take my horse to the old town road.")
    title: WishTitleField = Field(..., example="Horse")


class CreateWishResponse(Schema):
    id: IdField = Field(..., example=17)  # noqa: A003
    account_id: IdField = Field(..., example=42)
    avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
    created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
    description: WishDescriptionField = Field(..., example="I'm gonna take my horse to the old town road.")
    title: WishTitleField = Field(..., example="Horse")


class UpdateWishRequest(Schema):
    avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
    description: WishDescriptionField = Field(..., example="I'm gonna take my NEW horse to the old town road.")
    title: WishTitleField = Field(..., example="NEW Horse")


class UpdateWishResponse(Schema):
    id: IdField = Field(..., example=17)  # noqa: A003
    account_id: IdField = Field(..., example=42)
    avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
    created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
    description: WishDescriptionField = Field(..., example="I'm gonna take my NEW horse to the old town road.")
    title: WishTitleField = Field(..., example="NEW Horse")


class GetAccountWishesResponse(Schema):
    wishes: list[_Wish]
    class _Wish(Schema):  # noqa: E301
        id: IdField = Field(..., example=17)  # noqa: A003
        account_id: IdField = Field(..., example=42)
        avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
        created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
        description: WishDescriptionField = Field(..., example="I'm gonna take my horse to the old town road.")
        title: WishTitleField = Field(..., example="Horse")


class CreateWishBookingRequest(Schema):
    account_id: IdField = Field(..., example=42)


class CreateWishBookingResponse(Schema):
    account_id: IdField = Field(..., example=42)
    created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
    wish_id: IdField = Field(..., example=17)


class GetWishBookingsResponse(Schema):
    wish_bookings: list[_WishBooking]
    class _WishBooking(Schema):  # noqa: E301
        id: IdField = Field(..., example=1)  # noqa: A003
        account_id: IdField = Field(..., example=42)
        created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
        wish_id: IdField = Field(..., example=18)
