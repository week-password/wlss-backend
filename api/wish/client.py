from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.wish.dtos import (
    CreateWishBookingResponse,
    CreateWishResponse,
    GetAccountWishesResponse,
    GetWishBookingsResponse,
    UpdateWishResponse,
)


if TYPE_CHECKING:
    from typing import Self

    from wlss.shared.types import Id

    from api.wish.dtos import CreateWishBookingRequest, CreateWishRequest, UpdateWishRequest


class Wish:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create_wish(
        self: Self,
        account_id: Id,
        request_data: CreateWishRequest,
        token: str,
    ) -> CreateWishResponse:
        async with self._client as client:
            response = await client.post(
                f"/accounts/{account_id.value}/wishes",
                json=request_data.model_dump(),
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return CreateWishResponse.model_validate(response.json())

    async def update_wish(
        self: Self,
        account_id: Id,
        wish_id: Id,
        request_data: UpdateWishRequest,
        token: str,
    ) -> UpdateWishResponse:
        async with self._client as client:
            response = await client.put(
                f"/accounts/{account_id.value}/wishes/{wish_id.value}",
                json=request_data.model_dump(),
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return UpdateWishResponse.model_validate(response.json())

    async def delete_wish(self: Self, account_id: Id, wish_id: Id, token: str) -> None:
        async with self._client as client:
            response = await client.delete(
                f"/accounts/{account_id.value}/wishes/{wish_id.value}",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.NO_CONTENT

    async def get_account_wishes(self: Self, account_id: Id, token: str) -> GetAccountWishesResponse:
        async with self._client as client:
            response = await client.get(
                f"/accounts/{account_id.value}/wishes",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetAccountWishesResponse.model_validate(response.json())

    async def create_wish_booking(
        self: Self,
        account_id: Id,
        wish_id: Id,
        request_data: CreateWishBookingRequest,
        token: str,
    ) -> CreateWishBookingResponse:
        async with self._client as client:
            response = await client.post(
                f"/accounts/{account_id.value}/wishes/{wish_id.value}/bookings",
                json=request_data.model_dump(),
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return CreateWishBookingResponse.model_validate(response.json())

    async def get_wish_bookings(self: Self, account_id: Id, token: str) -> GetWishBookingsResponse:
        async with self._client as client:
            response = await client.get(
                f"/accounts/{account_id.value}/wishes/bookings",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetWishBookingsResponse.model_validate(response.json())

    async def delete_wish_booking(self: Self, account_id: Id, wish_id: Id, booking_id: Id, token: str) -> None:
        async with self._client as client:
            response = await client.delete(
                f"/accounts/{account_id.value}/wishes/{wish_id.value}/bookings/{booking_id.value}",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.NO_CONTENT
