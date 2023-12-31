"""Schemas for account related functionality."""

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
    """Existing account model."""

    id: PositiveInt  # noqa: A003

    created_at: datetime
    email: str
    login: str


class NewAccountWithProfile(Schema):
    """Account and corresponding profile data which are going to be created during sign up process."""

    account: NewAccount
    profile: NewProfile


class AccountWithProfile(Schema):
    """Account and corresponding profile which have been created during sign up process."""

    account: Account
    profile: Profile


class AccountId(Schema):
    """Account Id."""

    id: PositiveInt  # noqa: A003


class AccountLogin(Schema):
    """Account login."""

    login: str


class AccountEmail(Schema):
    """Account email."""

    email: str
