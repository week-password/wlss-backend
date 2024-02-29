from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.profile import schemas


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.shared.types import Id


async def get_profile(
    account_id: Id,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> schemas.Profile:
    account = await Account.get(session, account_id)
    profile = await account.get_profile(session)
    return schemas.Profile(
        account_id=account.id,
        avatar_id=profile.avatar_id,
        description=profile.description,
        name=profile.name,
    )


async def update_profile(
    account_id: Id,
    profile_update: schemas.ProfileUpdate,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> schemas.Profile:
    account = await Account.get(session, account_id)
    profile = await account.get_profile(session)
    profile = await profile.update(session, profile_update)
    return schemas.Profile(
        account_id=account.id,
        avatar_id=profile.avatar_id,
        description=profile.description,
        name=profile.name,
    )
