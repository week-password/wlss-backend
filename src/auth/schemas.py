from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import jwt
from pydantic import Field
from wlss.shared.types import UtcDatetime

from api.account.fields import AccountEmailField, AccountLoginField, AccountPasswordField
from api.shared.fields import IdField, UtcDatetimeField, UuidField
from api.shared.schemas import Schema
from src.config import CONFIG


if TYPE_CHECKING:
    from typing import Self


class Credentials(Schema):
    email: AccountEmailField | None = None
    login: AccountLoginField | None = None
    password: AccountPasswordField


class AccessTokenPayload(Schema):
    account_id: IdField
    expires_at: UtcDatetimeField = Field(
        default_factory=lambda: UtcDatetime(
            datetime.now(tz=timezone.utc)
            + timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION),
        ),
    )
    session_id: UuidField

    @classmethod
    def decode(cls: type[AccessTokenPayload], token: str) -> AccessTokenPayload:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, ["HS256"])
        return cls.model_validate(payload)

    def encode(self: Self) -> str:
        payload = self.model_dump()
        return jwt.encode(payload, CONFIG.SECRET_KEY, algorithm="HS256")


class RefreshTokenPayload(Schema):
    account_id: IdField
    expires_at: UtcDatetimeField = Field(
        default_factory=lambda: UtcDatetime(
            datetime.now(tz=timezone.utc)
            + timedelta(days=CONFIG.DAYS_BEFORE_REFRESH_TOKEN_EXPIRATION),
        ),
    )
    session_id: UuidField

    @classmethod
    def decode(cls: type[RefreshTokenPayload], token: str) -> RefreshTokenPayload:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, ["HS256"])
        return cls.model_validate(payload)

    def encode(self: Self) -> str:
        payload = self.model_dump()
        return jwt.encode(payload, CONFIG.SECRET_KEY, algorithm="HS256")
