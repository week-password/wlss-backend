from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.account.dtos import (
    CreateAccountResponse,
    GetAccountIdResponse,
)


if TYPE_CHECKING:
    from typing import Self

    from wlss.account.types import AccountLogin

    from api.account.dtos import (
        CreateAccountRequest,
        MatchAccountEmailRequest,
        MatchAccountLoginRequest,
    )


class Account:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create_account(self: Self, request_data: CreateAccountRequest) -> CreateAccountResponse:
        async with self._client as client:
            response = await client.post("/accounts", json=request_data.model_dump())
        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return CreateAccountResponse.model_validate(response.json())

    async def get_account_id(self: Self, account_login: AccountLogin, token: str) -> GetAccountIdResponse:
        async with self._client as client:
            response = await client.get(
                f"/accounts/logins/{account_login.value}/id",
                headers={"Authorization": f"Bearer {token}"},
            )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetAccountIdResponse.model_validate(response.json())

    async def match_account_login(self: Self, request_data: MatchAccountLoginRequest) -> bool:
        async with self._client as client:
            response = await client.post(
                "/accounts/logins/match",
                json=request_data.model_dump(),
            )
        response.raise_for_status()
        return response.status_code == httpx.codes.NO_CONTENT

    async def match_account_email(self: Self, request_data: MatchAccountEmailRequest) -> bool:
        async with self._client as client:
            response = await client.post(
                "/accounts/emails/match",
                json=request_data.model_dump(),
            )
        response.raise_for_status()
        return response.status_code == httpx.codes.NO_CONTENT
