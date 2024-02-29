from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.account import controllers, schemas
from src.account.fields import AccountLoginField
from src.account.models import Account
from src.auth.dependencies import get_account_from_access_token
from src.shared import swagger as shared_swagger
from src.shared.database import get_session


router = APIRouter(tags=["account"])


@router.post(
    "/accounts",
    description="Sign Up - create a new account with profile.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "New account and profile are created.",
            "content": {
                "application/json": {
                    "example": {
                        "account": {
                            "id": 42,
                            "email": "john.doe@mail.com",
                            "login": "john_doe",
                            "created_at": "2023-06-17T11:47:02.823Z",
                        },
                        "profile": {
                            "account_id": 42,
                            "avatar_id": None,
                            "description": "Who da heck is John Doe?",
                            "name": "John Doe",
                        },
                    },
                },
            },
        },
    },
    response_model=schemas.AccountWithProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Sign Up - create a new account.",
)
async def create_account(
    new_account: Annotated[
        schemas.NewAccountWithProfile,
        Body(
            example={
                "account": {
                    "email": "john.doe@mail.com",
                    "login": "john_doe",
                    "password": "qwerty123",
                },
                "profile": {
                    "name": "John Doe",
                    "description": "Who da heck is John Doe?",
                },
            },
        ),
    ],
    session: AsyncSession = Depends(get_session),
) -> schemas.AccountWithProfile:
    return await controllers.create_account(new_account, session)


@router.get(
    "/accounts/logins/{account_login}/id",
    description="Get Account Id by login. Account Id is available for every logged in user.",
    responses={
        status.HTTP_200_OK: {
            "description": "Account Id returned",
            "content": {
                "application/json": {
                    "example": {
                        "id": 42,
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.AccountId,
    status_code=status.HTTP_200_OK,
    summary="Get Account Id.",
)
async def get_account_id(
    account_login: Annotated[AccountLoginField, Path(example="john_doe")],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> schemas.AccountId:
    return await controllers.get_account_id(account_login, current_account, session)


@router.post(
    "/accounts/logins/match",
    description="Check if account with provided login exists.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Account with current login exists.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Account with current login doesn't exist.",
        },
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Check login uniqueness.",
)
async def match_account_login(
    account_login: Annotated[schemas.AccountLogin, Body(example={"login": "john_doe"})],
    session: AsyncSession = Depends(get_session),
) -> None:
    await controllers.match_account_login(account_login, session)


@router.post(
    "/accounts/emails/match",
    description="Check if account with provided email exists.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Account with current email exists.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Account with current email doesn't exist.",
        },
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Check email uniqueness.",
)
async def match_account_email(
    account_email: Annotated[schemas.AccountEmail, Body(example={"email": "john.doe@mail.com"})],
    session: AsyncSession = Depends(get_session),
) -> None:
    await controllers.match_account_email(account_email, session)
