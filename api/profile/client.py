from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.profile.dtos import GetProfileResponse, GetProfilesResponse, UpdateProfileResponse


if TYPE_CHECKING:
    from typing import Self

    from wlss.shared.types import Id

    from api.profile.dtos import UpdateProfileRequest


class Profile:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_profile(self: Self, account_id: Id, token: str) -> GetProfileResponse:
        async with self._client as client:
            response = await client.get(
                f"/accounts/{account_id.value}/profile",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetProfileResponse.model_validate(response.json())

    async def update_profile(
        self: Self,
        account_id: Id,
        request_data: UpdateProfileRequest,
        token: str,
    ) -> UpdateProfileResponse:
        async with self._client as client:
            response = await client.put(
                f"/accounts/{account_id.value}/profile",
                json=request_data.model_dump(),
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return UpdateProfileResponse.model_validate(response.json())

    async def get_profiles(self: Self, account_ids: list[Id], token: str) -> GetProfilesResponse:
        async with self._client as client:
            response = await client.get(
                "/profiles",
                params={"account_id": [account_id.value for account_id in account_ids]},
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetProfilesResponse.model_validate(response.json())
