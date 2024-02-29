from __future__ import annotations

from uuid import UUID

from src.profile.fields import ProfileDescriptionField, ProfileNameField
from src.shared.fields import IdField, UuidField
from src.shared.schemas import Schema


class NewProfile(Schema):
    name: ProfileNameField
    description: ProfileDescriptionField | None = None


class Profile(Schema):
    account_id: IdField

    avatar_id: UUID | None = None
    description: ProfileDescriptionField | None = None
    name: ProfileNameField


class ProfileUpdate(Schema):
    avatar_id: UuidField | None = None
    description: ProfileDescriptionField | None = None
    name: ProfileNameField
