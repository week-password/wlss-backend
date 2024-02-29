from __future__ import annotations

from typing import TYPE_CHECKING

from src.account import schemas
from src.account.models import Account, PasswordHash
from src.profile.models import Profile


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.account.types import AccountLogin

    from src.account.schemas import NewAccountWithProfile


async def create_account(request_data: NewAccountWithProfile, session: AsyncSession) -> schemas.AccountWithProfile:
    account = await Account.create(session, request_data.account)
    profile = await Profile.create(session, request_data.profile, account_id=account.id)
    await PasswordHash.create(session, request_data.account.password, account_id=account.id)
    return schemas.AccountWithProfile.model_validate({"account": account, "profile": profile}, from_attributes=True)


async def get_account_id(
    account_login: AccountLogin,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> schemas.AccountId:
    account = await Account.get_by_login(session, account_login)
    return schemas.AccountId(id=account.id)


async def match_account_login(account_login: schemas.AccountLogin, session: AsyncSession) -> None:
    await Account.get_by_login(session, account_login.login)


async def match_account_email(account_email: schemas.AccountEmail, session: AsyncSession) -> None:
    await Account.get_by_email(session, account_email.email)
