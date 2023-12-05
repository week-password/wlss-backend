"""Schemas for profile related functionality."""

from __future__ import annotations

from uuid import UUID

from pydantic import PositiveInt

from src.profile.fields import Description, Name
from src.shared.schemas import Schema


class NewProfile(Schema):
    """Profile data for an account which is going to be created during sign up process."""

    name: Name
    description: Description | None


class Profile(Schema):
    """Account profile."""

    account_id: PositiveInt

    avatar_id: UUID | None
    description: Description | None
    name: Name

    class Config:
        """Pydantic's special class to configure pydantic models."""

        orm_mode = True


class ProfileUpdate(Schema):
    """Data for Profile update."""

    avatar_id: UUID | None
    description: Description | None
    name: Name
