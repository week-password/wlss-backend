from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.auth.dtos import CreateSessionResponse, RefreshTokensResponse


if TYPE_CHECKING:
    from typing import Self
    from uuid import UUID

    from wlss.shared.types import Id

    from api.auth.dtos import CreateSessionRequest


class Auth:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create_session(self: Self, request_data: CreateSessionRequest) -> CreateSessionResponse:
        async with self._client as client:
            response = await client.post("/sessions", json=request_data.model_dump())
        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return CreateSessionResponse.model_validate(response.json())

    async def refresh_tokens(self: Self, account_id: Id, session_id: UUID, token: str) -> RefreshTokensResponse:
        async with self._client as client:
            response = await client.post(
                f"/accounts/{account_id.value}/sessions/{session_id}/tokens",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return RefreshTokensResponse.model_validate(response.json())

    async def delete_session(self: Self, account_id: Id, session_id: UUID, token: str) -> None:
        async with self._client as client:
            response = await client.delete(
                f"/accounts/{account_id.value}/sessions/{session_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.NO_CONTENT

    async def delete_all_sessions(self: Self, account_id: Id, token: str) -> None:
        async with self._client as client:
            response = await client.delete(
                f"/accounts/{account_id.value}/sessions",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.NO_CONTENT
