from __future__ import annotations

from src.profile.fields import ProfileDescriptionField, ProfileNameField
from src.shared.fields import UuidField
from src.shared.schemas import Schema


class NewProfile(Schema):
    name: ProfileNameField
    description: ProfileDescriptionField | None = None


class ProfileUpdate(Schema):
    avatar_id: UuidField | None = None
    description: ProfileDescriptionField | None = None
    name: ProfileNameField
