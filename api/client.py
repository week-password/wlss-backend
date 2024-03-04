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


class Api:  # pylint: disable=too-many-instance-attributes
    def __init__(self: Self, app: Callable[..., Any] | None = None, base_url: str = "") -> None:
        self._client = httpx.AsyncClient(app=app, base_url=base_url)

        self._account = Account(self._client)
        self._auth = Auth(self._client)
        self._file = File(self._client)
        self._friendship = Friendship(self._client)
        self._health = Health(self._client)
        self._profile = Profile(self._client)
        self._wish = Wish(self._client)

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
