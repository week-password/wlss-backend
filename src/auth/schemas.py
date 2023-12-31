"""Auth related schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any, TypeVar
from uuid import UUID

from pydantic import model_validator, PositiveInt

from src.shared.schemas import Schema


DictT = TypeVar("DictT", bound=dict[str, Any])


class Credentials(Schema):
    """Account credentials for sign in process. Can be a pair of password and email or password and login."""

    email: str | None = None
    login: str | None = None
    password: str

    @model_validator(mode="before")
    @classmethod  # to silent mypy error, because mypy doesn't recognize model_validator as a classmethod
    def _require_login_or_email(cls: type[Credentials], values: DictT) -> DictT:  # pragma: no cover
        if not (values["login"] or values["email"]):
            msg = "Either 'login' or 'email' is required."
            raise ValueError(msg)
        return values

    @model_validator(mode="before")
    @classmethod  # to silent mypy error, because mypy doesn't recognize model_validator as a classmethod
    def _forbid_login_and_email_together(cls: type[Credentials], values: DictT) -> DictT:  # pragma: no cover
        if values["login"] and values["email"]:
            msg = "You cannot use 'login' and 'email' together. Choose one of them."
            raise ValueError(msg)
        return values


class Session(Schema):
    """Auth session attached to particular account."""

    id: UUID  # noqa: A003

    account_id: PositiveInt


class Tokens(Schema):
    """Generated access and refresh tokens for particular auth session."""

    access_token: str
    refresh_token: str


class SessionWithTokens(Schema):
    """Auth session with tokens generated for it."""

    session: Session
    tokens: Tokens


class AccessTokenPayload(Schema):
    """Access token payload schema."""

    account_id: PositiveInt
    created_at: datetime
    session_id: PositiveInt


class RefreshTokenPayload(Schema):
    """Refresh token payload schema."""

    created_at: datetime
    session_id: PositiveInt
