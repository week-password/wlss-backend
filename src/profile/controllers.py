from __future__ import annotations

from typing import TYPE_CHECKING

from api.profile.dtos import GetProfileResponse, GetProfilesResponse, SearchProfilesResponse, UpdateProfileResponse
from src.account.models import Account
from src.profile.models import Profile
from src.profile.schemas import ProfileUpdate


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.shared.types import Id

    from api.profile.dtos import UpdateProfileRequest


async def get_profile(
    account_id: Id,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> GetProfileResponse:
    account = await Account.get(session, account_id)
    profile = await account.get_profile(session)
    return GetProfileResponse.model_validate(profile, from_attributes=True)


async def update_profile(
    account_id: Id,
    request_data: UpdateProfileRequest,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> UpdateProfileResponse:
    account = await Account.get(session, account_id)
    profile = await account.get_profile(session)
    profile_update = ProfileUpdate.from_(request_data)
    profile = await profile.update(session, profile_update)
    return UpdateProfileResponse.model_validate(profile, from_attributes=True)


async def get_profiles(
    account_ids: list[Id],
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> GetProfilesResponse:
    profiles = await Profile.get_multiple(session, account_ids)
    return GetProfilesResponse.model_validate({"profiles": profiles}, from_attributes=True)


async def search_profiles(
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> SearchProfilesResponse:
    profiles = await Profile.search_profiles(session)
    return SearchProfilesResponse.model_validate({"profiles": profiles}, from_attributes=True)
