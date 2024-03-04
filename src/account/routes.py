from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.account.dtos import (
    CreateAccountRequest,
    CreateAccountResponse,
    GetAccountIdResponse,
    MatchAccountEmailRequest,
    MatchAccountLoginRequest,
)
from api.account.fields import AccountLoginField
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
    "/accounts/logins/{account_login}/id",
    description="Get account id by login. Account id is available for every logged in user.",
    responses={
        status.HTTP_200_OK: {"description": "Account id returned"},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Get account id.",
)
async def get_account_id(
    account_login: Annotated[AccountLoginField, Path(example="john_doe")],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> GetAccountIdResponse:
    return await controllers.get_account_id(account_login, current_account, session)


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
