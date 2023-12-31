"""Schemas for profile related functionality."""

from __future__ import annotations

from uuid import UUID

from pydantic import PositiveInt

from src.shared.schemas import Schema


class NewProfile(Schema):
    """Profile data for an account which is going to be created during sign up process."""

    name: str
    description: str | None = None


class Profile(Schema):
    """Account profile."""

    account_id: PositiveInt

    avatar_id: UUID | None = None
    description: str | None = None
    name: str


class ProfileUpdate(Schema):
    """Data for Profile update."""

    avatar_id: UUID | None = None
    description: str | None = None
    name: str
