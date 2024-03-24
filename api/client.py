from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from api.account.client import Account
from api.auth.client import Auth
from api.file.client import File
from api.friendship.client import Friendship
from api.health.client import Health
from api.profile.client import Profile
from api.wish.client import Wish


if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Self


class Api:
    def __init__(
        self: Self,
        app: Callable[..., Any] | None = None,
        base_url: str = "",
        timeout: httpx.Timeout = httpx.Timeout(30),  # noqa: B008
    ) -> None:
        self._client = httpx.AsyncClient(app=app, base_url=base_url, timeout=timeout)

    async def __aenter__(self: Self) -> Client:
        return Client(await self._client.__aenter__())

    async def __aexit__(self: Self, *args: Any, **kwargs: Any) -> None:
        await self._client.__aexit__(*args, **kwargs)


class Client:
    def __init__(self: Self, connection: httpx.AsyncClient) -> None:

        self._account = Account(connection)
        self._auth = Auth(connection)
        self._file = File(connection)
        self._friendship = Friendship(connection)
        self._health = Health(connection)
        self._profile = Profile(connection)
        self._wish = Wish(connection)

    @property
    def account(self: Self) -> Account:
        return self._account

    @property
    def auth(self: Self) -> Auth:
        return self._auth

    @property
    def file(self: Self) -> File:
        return self._file

    @property
    def friendship(self: Self) -> Friendship:
        return self._friendship

    @property
    def health(self: Self) -> Health:
        return self._health

    @property
    def profile(self: Self) -> Profile:
        return self._profile

    @property
    def wish(self: Self) -> Wish:
        return self._wish
