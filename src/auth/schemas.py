from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, TYPE_CHECKING, TypeVar
from uuid import UUID

import jwt
from pydantic import Field, field_serializer, model_validator, PositiveInt

from src.config import CONFIG
from src.shared.schemas import Schema


if TYPE_CHECKING:
    from typing import Self


DictT = TypeVar("DictT", bound=dict[str, Any])


class Credentials(Schema):
    email: str | None = None
    login: str | None = None
    password: str

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
    id: UUID  # noqa: A003

    account_id: PositiveInt


class Tokens(Schema):
    access_token: str
    refresh_token: str


class SessionWithTokens(Schema):
    session: Session
    tokens: Tokens


class AccessTokenPayload(Schema):
    account_id: PositiveInt
    expires_at: datetime = Field(
        default_factory=lambda: (
            datetime.now(tz=timezone.utc)
            + timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION)
        ),
    )
    session_id: UUID

    @field_serializer("expires_at")
    def _serialize_datetime(self: Self, value: datetime) -> str:  # pylint: disable=no-self-use
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @field_serializer("session_id")
    def _serialize_uuid(self: Self, value: UUID) -> str:  # pylint: disable=no-self-use
        return str(value)

    @classmethod
    def decode(cls: type[AccessTokenPayload], token: str) -> AccessTokenPayload:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, ["HS256"])
        return cls.model_validate(payload)

    def encode(self: Self) -> str:
        payload = self.model_dump()
        return jwt.encode(payload, CONFIG.SECRET_KEY, algorithm="HS256")


class RefreshTokenPayload(Schema):
    account_id: PositiveInt
    expires_at: datetime = Field(
        default_factory=lambda: (
            datetime.now(tz=timezone.utc)
            + timedelta(days=CONFIG.DAYS_BEFORE_REFRESH_TOKEN_EXPIRATION)
        ),
    )
    session_id: UUID

    @field_serializer("expires_at")
    def _serialize_datetime(self: Self, value: datetime) -> str:  # pylint: disable=no-self-use
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @field_serializer("session_id")
    def _serialize_uuid(self: Self, value: UUID) -> str:  # pylint: disable=no-self-use
        return str(value)

    @classmethod
    def decode(cls: type[RefreshTokenPayload], token: str) -> RefreshTokenPayload:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, ["HS256"])
        return cls.model_validate(payload)

    def encode(self: Self) -> str:
        payload = self.model_dump()
        return jwt.encode(payload, CONFIG.SECRET_KEY, algorithm="HS256")
