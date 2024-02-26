from __future__ import annotations

from uuid import UUID

from pydantic import PositiveInt

from src.shared.schemas import Schema


class NewProfile(Schema):
    name: str
    description: str | None = None


class Profile(Schema):
    account_id: PositiveInt

    avatar_id: UUID | None = None
    description: str | None = None
    name: str


class ProfileUpdate(Schema):
    avatar_id: UUID | None = None
    description: str | None = None
    name: str
