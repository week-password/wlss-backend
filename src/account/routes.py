from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.account.dtos import (
    CreateAccountRequest,
    CreateAccountResponse,
    GetAccountResponse,
    GetAccountsResponse,
    MatchAccountEmailRequest,
    MatchAccountLoginRequest,
)
from api.account.fields import AccountLoginField
from api.shared.fields import IdField
from src.account import controllers
from src.account.models import Account
from src.auth.dependencies import get_account_from_access_token
from src.shared import swagger as shared_swagger
from src.shared.database import get_session


router = APIRouter(tags=["account"])


@router.post(
    "/accounts",
    description="Sign Up - create a new account with profile.",
    responses={
        status.HTTP_201_CREATED: {"description": "New account and profile are created."},
    },
    status_code=status.HTTP_201_CREATED,
    summary="Sign Up - create a new account.",
)
async def create_account(
    request_data: Annotated[CreateAccountRequest, Body()],
    session: AsyncSession = Depends(get_session),
) -> CreateAccountResponse:
    return await controllers.create_account(request_data, session)


@router.get(
    "/accounts/{account_id}",
    description="Get account. Returns public available info for particular account",
    responses={
        status.HTTP_200_OK: {"description": "Account info returned"},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Get account.",
)
async def get_account(
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    account_id: Annotated[IdField, Path(example=42)],
    session: AsyncSession = Depends(get_session),
) -> GetAccountResponse:
    return await controllers.get_account(account_id, current_account, session)


@router.get(
    "/accounts",
    description="Get accounts. Account infos are available for every logged in user.",
    responses={
        status.HTTP_200_OK: {"description": "Accounts info returned"},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Get accounts.",
)
async def get_accounts(
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    account_ids: Annotated[
        list[IdField],
        Query(alias="account_id", example=[42, 18]),
    ] = [],  # noqa: B006
    account_logins: Annotated[
        list[AccountLoginField],
        Query(alias="account_login", example=["john", "bob"]),
    ] = [],  # noqa: B006
    session: AsyncSession = Depends(get_session),
) -> GetAccountsResponse:
    return await controllers.get_accounts(account_ids, account_logins, current_account, session)


@router.post(
    "/accounts/logins/match",
    description="Check if account with provided login exists.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Account with current login exists."},
        status.HTTP_404_NOT_FOUND: {"description": "Account with current login doesn't exist."},
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Check login uniqueness.",
)
async def match_account_login(
    request_data: Annotated[MatchAccountLoginRequest, Body()],
    session: AsyncSession = Depends(get_session),
) -> None:
    await controllers.match_account_login(request_data, session)


@router.post(
    "/accounts/emails/match",
    description="Check if account with provided email exists.",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Account with current email exists."},
        status.HTTP_404_NOT_FOUND: {"description": "Account with current email doesn't exist."},
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Check email uniqueness.",
)
async def match_account_email(
    request_data: Annotated[MatchAccountEmailRequest, Body()],
    session: AsyncSession = Depends(get_session),
) -> None:
    await controllers.match_account_email(request_data, session)
