from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, TYPE_CHECKING, TypeVar

import jwt
from pydantic import Field, model_validator
from wlss.shared.types import UtcDatetime

from src.account.fields import AccountEmailField, AccountLoginField, AccountPasswordField
from src.config import CONFIG
from src.shared.fields import IdField, UtcDatetimeField, UuidField
from src.shared.schemas import Schema


if TYPE_CHECKING:
    from typing import Self


DictT = TypeVar("DictT", bound=dict[str, Any])


class Credentials(Schema):
    email: AccountEmailField | None = None
    login: AccountLoginField | None = None
    password: AccountPasswordField

    @model_validator(mode="before")
    @classmethod  # to silent mypy error, because mypy doesn't recognize model_validator as a classmethod
    def _require_login_or_email(cls: type[Credentials], values: DictT) -> DictT:  # pragma: no cover
        if not (values.get("login") or values.get("email")):
            msg = "Either 'login' or 'email' is required."
            raise ValueError(msg)
        return values

    @model_validator(mode="before")
    @classmethod  # to silent mypy error, because mypy doesn't recognize model_validator as a classmethod
    def _forbid_login_and_email_together(cls: type[Credentials], values: DictT) -> DictT:  # pragma: no cover
        if values.get("login") and values.get("email"):
            msg = "You cannot use 'login' and 'email' together. Choose one of them."
            raise ValueError(msg)
        return values


class Session(Schema):
    id: UuidField  # noqa: A003

    account_id: IdField


class Tokens(Schema):
    access_token: str
    refresh_token: str


class SessionWithTokens(Schema):
    session: Session
    tokens: Tokens


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
