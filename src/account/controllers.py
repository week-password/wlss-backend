from __future__ import annotations

from typing import TYPE_CHECKING

from api.account.dtos import CreateAccountResponse, GetAccountResponse, GetAccountsResponse
from src.account.models import Account, PasswordHash
from src.account.schemas import NewAccount
from src.profile.models import Profile
from src.profile.schemas import NewProfile


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.account.types import AccountLogin
    from wlss.shared.types import Id

    from api.account.dtos import CreateAccountRequest, MatchAccountEmailRequest, MatchAccountLoginRequest


async def create_account(request_data: CreateAccountRequest, session: AsyncSession) -> CreateAccountResponse:
    new_account = NewAccount.from_(request_data.account)
    account = await Account.create(session, new_account)

    new_profile = NewProfile.from_(request_data.profile)
    profile = await Profile.create(session, new_profile, account=account)

    await PasswordHash.create(session, request_data.account.password, account=account)
    return CreateAccountResponse.model_validate({"account": account, "profile": profile}, from_attributes=True)


async def get_account(
    account_id: Id,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> GetAccountResponse:
    account = await Account.get(session, account_id)
    return GetAccountResponse.model_validate(account, from_attributes=True)


async def get_accounts(
    account_ids: list[Id],
    account_logins: list[AccountLogin],
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> GetAccountsResponse:
    accounts = await Account.get_accounts(session, account_ids, account_logins)
    return GetAccountsResponse.model_validate({"accounts": accounts}, from_attributes=True)


async def match_account_login(request_data: MatchAccountLoginRequest, session: AsyncSession) -> None:
    await Account.get_by_login(session, request_data.login)


async def match_account_email(request_data: MatchAccountEmailRequest, session: AsyncSession) -> None:
    await Account.get_by_email(session, request_data.email)
