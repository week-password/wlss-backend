from __future__ import annotations

from pydantic import Field

from api.profile.fields import ProfileDescriptionField, ProfileNameField
from api.shared.fields import IdField, UuidField
from api.shared.schemas import Schema


class GetProfileResponse(Schema):
    account_id: IdField = Field(..., example=42)
    avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
    description: ProfileDescriptionField | None = Field(..., example="Who da heck is John Doe?")
    name: ProfileNameField = Field(..., example="John Doe")


class UpdateProfileRequest(Schema):
    avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
    description: ProfileDescriptionField | None = Field(..., example="NEW John Doe's profile description.")
    name: ProfileNameField = Field(..., example="NEW John Doe's profile name.")


class UpdateProfileResponse(Schema):
    account_id: IdField = Field(..., example=42)
    avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
    description: ProfileDescriptionField | None = Field(..., example="NEW John Doe's profile description.")
    name: ProfileNameField = Field(..., example="NEW John Doe's profile name.")


class GetProfilesResponse(Schema):
    profiles: list[_Profile]
    class _Profile(Schema):  # noqa: E301
        account_id: IdField = Field(..., example=42)
        avatar_id: UuidField | None = Field(..., example="0b928aaa-521f-47ec-8be5-396650e2a187")
        description: ProfileDescriptionField | None = Field(..., example="Who da heck is John Doe?")
        name: ProfileNameField = Field(..., example="John Doe")
