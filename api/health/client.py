from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.health.dtos import HealthResponse


if TYPE_CHECKING:
    from typing import Self


class Health:  # pylint: disable=too-few-public-methods
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_health(self: Self) -> HealthResponse:
        response = await self._client.get("/health")
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return HealthResponse.model_validate(response.json())
