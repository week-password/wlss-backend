from __future__ import annotations

from api.profile.fields import ProfileDescriptionField, ProfileNameField
from api.shared.fields import UuidField
from api.shared.schemas import Schema


class NewProfile(Schema):
    name: ProfileNameField
    description: ProfileDescriptionField | None = None


class ProfileUpdate(Schema):
    avatar_id: UuidField | None = None
    description: ProfileDescriptionField | None = None
    name: ProfileNameField
