"""Schemas for profile related functionality."""

from __future__ import annotations

from pydantic import PositiveInt

from src.profile.fields import Avatar, Description, Name
from src.shared.schemas import Schema


class Profile(Schema):
    """Account profile."""

    account_id: PositiveInt

    avatar: Avatar | None
    description: Description | None
    name: Name