"""Controllers functions for account entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.account import schemas as account_schemas
from src.account.models import Account, PasswordHash
from src.auth import schemas
from src.profile import schemas as profile_schemas
from src.profile.models import Profile


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.auth.schemas import NewAccountWithProfile


async def create_account(request_data: NewAccountWithProfile, session: AsyncSession) -> schemas.AccountWithProfile:
    """Create a new account with profile."""
    account = await Account.create(session, request_data.account)
    profile = await Profile.create(session, request_data.profile, account_id=account.id)
    await PasswordHash.create(session, request_data.account.password, account_id=account.id)
    return schemas.AccountWithProfile(
        account=account_schemas.Account.from_orm(account),
        profile=profile_schemas.Profile.from_orm(profile),
    )
