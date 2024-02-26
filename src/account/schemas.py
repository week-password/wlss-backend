from __future__ import annotations

from datetime import datetime

from pydantic import PositiveInt

from src.profile.schemas import NewProfile, Profile
from src.shared.schemas import Schema


class NewAccount(Schema):
    """Account data which is going to be created during sign up process."""

    email: str
    login: str
    password: str


class Account(Schema):
    id: PositiveInt  # noqa: A003

    created_at: datetime
    email: str
    login: str


class NewAccountWithProfile(Schema):
    account: NewAccount
    profile: NewProfile


class AccountWithProfile(Schema):
    account: Account
    profile: Profile


class AccountId(Schema):
    id: PositiveInt  # noqa: A003


class AccountLogin(Schema):
    login: str


class AccountEmail(Schema):
    email: str
