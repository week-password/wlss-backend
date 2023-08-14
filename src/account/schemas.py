"""Schemas for account related functionality."""

from __future__ import annotations

from datetime import datetime

from pydantic import PositiveInt

from src.account.fields import Email, Login
from src.shared.schemas import Schema


class Account(Schema):
    """Existing account model."""

    id: PositiveInt  # noqa: A003

    created_at: datetime
    email: Email
    login: Login


class AccountId(Schema):
    """Account Id."""

    id: PositiveInt  # noqa: A003


class AccountLogin(Schema):
    """Account login."""

    login: Login


class AccountEmail(Schema):
    """Account email."""

    email: Email
