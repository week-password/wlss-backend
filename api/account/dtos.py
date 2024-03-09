from __future__ import annotations

from pydantic import Field

from api.account.fields import AccountEmailField, AccountLoginField, AccountPasswordField
from api.profile.fields import ProfileDescriptionField, ProfileNameField
from api.shared.fields import IdField, UtcDatetimeField, UuidField
from api.shared.schemas import Schema


class CreateAccountRequest(Schema):
    account: _Account
    class _Account(Schema):  # noqa: E301
        email: AccountEmailField = Field(..., example="john.doe@mail.com")
        login: AccountLoginField = Field(..., example="john_doe")
        password: AccountPasswordField = Field(..., example="qwerty123")

    profile: _Profile
    class _Profile(Schema):  # noqa: E301
        name: ProfileNameField = Field(..., example="John Doe")
        description: ProfileDescriptionField | None = Field(None, example="Who da heck is John Doe?")


class CreateAccountResponse(Schema):
    account: _Account
    class _Account(Schema):  # noqa: E301
        id: IdField = Field(..., example=42)  # noqa: A003
        created_at: UtcDatetimeField = Field(..., example="2023-06-17T11:47:02.823Z")
        email: AccountEmailField = Field(..., example="john.doe@mail.com")
        login: AccountLoginField = Field(..., example="john_doe")

    profile: _Profile
    class _Profile(Schema):  # noqa: E301
        account_id: IdField = Field(..., example=42)
        avatar_id: UuidField | None = Field(..., example=None)
        description: ProfileDescriptionField | None = Field(..., example="Who da heck is John Doe?")
        name: ProfileNameField = Field(..., example="John Doe")


class GetAccountResponse(Schema):
    id: IdField = Field(..., example=42)  # noqa: A003
    login: AccountLoginField = Field(..., example="john_doe")


class GetAccountsResponse(Schema):
    accounts: list[_Account]
    class _Account(Schema):  # noqa: E301
        id: IdField = Field(..., example=42)  # noqa: A003
        login: AccountLoginField = Field(..., example="john_doe")


class MatchAccountLoginRequest(Schema):
    login: AccountLoginField = Field(..., example="john_doe")


class MatchAccountEmailRequest(Schema):
    email: AccountEmailField = Field(..., example="john.doe@mail.com")
