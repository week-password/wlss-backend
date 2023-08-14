"""Account related endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.security import HTTPAuthorizationCredentials

from src.account import schemas
from src.account.fields import Login
from src.auth import swagger as auth_swagger
from src.auth.security import get_token
from src.shared import swagger as shared_swagger


router = APIRouter(tags=["account"])


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
        status.HTTP_401_UNAUTHORIZED: auth_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.AccountId,
    status_code=status.HTTP_200_OK,
    summary="Get Account Id.",
)
async def get_account_id(
    account_login: Annotated[Login, Path(example="john_doe")],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get Account Id by Login."""


@router.get(
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
    account_login: Annotated[schemas.AccountLogin, Body(example={"login": "john_doe"})],  # noqa: ARG001
) -> None:
    """Check account login uniqueness."""


@router.get(
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
    account_email: Annotated[schemas.AccountEmail, Body(example={"email": "john.doe@mail.com"})],  # noqa: ARG001
) -> None:
    """Check account email uniqueness."""
