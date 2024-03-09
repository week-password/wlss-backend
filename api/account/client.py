from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.account.dtos import (
    CreateAccountResponse,
    GetAccountResponse,
    GetAccountsResponse,
)


if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Self

    from wlss.account.types import AccountLogin
    from wlss.shared.types import Id

    from api.account.dtos import (
        CreateAccountRequest,
        MatchAccountEmailRequest,
        MatchAccountLoginRequest,
    )


class Account:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create_account(self: Self, request_data: CreateAccountRequest) -> CreateAccountResponse:
        response = await self._client.post("/accounts", json=request_data.model_dump())
        response.raise_for_status()
        assert response.status_code == httpx.codes.CREATED
        return CreateAccountResponse.model_validate(response.json())

    async def get_account(
        self: Self,
        account_id: Id,
        token: str,
    ) -> GetAccountResponse:
        response = await self._client.get(f"/accounts/{account_id.value}", headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetAccountResponse.model_validate(response.json())

    async def get_accounts(
        self: Self,
        token: str,
        account_ids: Iterable[Id] | None = None,
        account_logins: Iterable[AccountLogin] | None = None,
    ) -> GetAccountsResponse:
        account_ids = account_ids or []
        account_logins = account_logins or []
        response = await self._client.get(
            "/accounts",
            params={
                "account_id": [str(v.value) for v in account_ids],
                "account_login": [v.value for v in account_logins],
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        assert response.status_code == httpx.codes.OK
        return GetAccountsResponse.model_validate(response.json())

    async def match_account_login(self: Self, request_data: MatchAccountLoginRequest) -> bool:
        response = await self._client.post(
            "/accounts/logins/match",
            json=request_data.model_dump(),
        )
        response.raise_for_status()
        return response.status_code == httpx.codes.NO_CONTENT

    async def match_account_email(self: Self, request_data: MatchAccountEmailRequest) -> bool:
        response = await self._client.post(
            "/accounts/emails/match",
            json=request_data.model_dump(),
        )
        response.raise_for_status()
        return response.status_code == httpx.codes.NO_CONTENT
