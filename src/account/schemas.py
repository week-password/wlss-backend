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
