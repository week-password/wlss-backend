"""Auth related schemas."""

from __future__ import annotations

from typing import Any, TypeVar
from uuid import UUID

from pydantic import root_validator

from src.account.fields import Email, Login
from src.account.schemas import Account
from src.auth.fields import Password
from src.profile.fields import Description, Name
from src.profile.schemas import Profile
from src.shared.schemas import Schema


DictT = TypeVar("DictT", bound=dict[str, Any])


class NewAccount(Schema):
    """Account data which is going to be created during sign up process."""

    email: Email
    login: Login
    password: Password


class NewProfile(Schema):
    """Profile data for an account which is going to be created during sign up process."""

    name: Name
    description: Description | None


class NewAccountWithProfile(Schema):
    """Account and corresponding profile data which are going to be created during sign up process."""

    account: NewAccount
    profile: NewProfile


class AccountWithProfile(Schema):
    """Account and corresponding profile which have been created during sign up process."""

    account: Account
    profile: Profile


class Credentials(Schema):
    """Account credentials for sign in process. Can be a pair of password and email or password and login."""

    email: Email | None
    login: Login | None
    password: Password

    @classmethod  # to silent mypy error, because mypy doesn't recognize root_validator as a classmethod
    @root_validator(pre=True)
    def _require_login_or_email(cls: type[Credentials], values: DictT) -> DictT:  # pragma: no cover
        if not (values["login"] or values["email"]):
            msg = "Either 'login' or 'email' is required."
            raise ValueError(msg)
        return values

    @classmethod  # to silent mypy error, because mypy doesn't recognize root_validator as a classmethod
    @root_validator(pre=True)
    def _forbid_login_and_email_together(cls: type[Credentials], values: DictT) -> DictT:  # pragma: no cover
        if values["login"] and values["email"]:
            msg = "You cannot use 'login' and 'email' together. Choose one of them."
            raise ValueError(msg)
        return values


class Tokens(Schema):
    """Account tokens attached to a particular device."""

    device_id: UUID
    access_token: str
    refresh_token: str


class RefreshToken(Schema):
    """Refresh token for a particular device."""

    device_id: UUID
    refresh_token: str
