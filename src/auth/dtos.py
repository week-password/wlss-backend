from __future__ import annotations

from typing import Any, TypeVar

from pydantic import Field, model_validator

from src.account.fields import AccountEmailField, AccountLoginField, AccountPasswordField
from src.shared.fields import IdField, UuidField
from src.shared.schemas import Schema


DictT = TypeVar("DictT", bound=dict[str, Any])


class CreateSessionRequest(Schema):
    email: AccountEmailField | None = Field(None, example="john.doe@mai.com")
    login: AccountLoginField | None = Field(None, example="john_doe")
    password: AccountPasswordField = Field(..., example="qwerty123")

    @model_validator(mode="before")
    @classmethod  # to silent mypy error, because mypy doesn't recognize model_validator as a classmethod
    def _require_login_or_email(cls: type[CreateSessionRequest], values: DictT) -> DictT:
        if not (values.get("login") or values.get("email")):
            msg = "Either 'login' or 'email' is required."
            raise ValueError(msg)
        return values

    @model_validator(mode="before")
    @classmethod  # to silent mypy error, because mypy doesn't recognize model_validator as a classmethod
    def _forbid_login_and_email_together(cls: type[CreateSessionRequest], values: DictT) -> DictT:
        if values.get("login") and values.get("email"):
            msg = "You cannot use 'login' and 'email' together. Choose one of them."
            raise ValueError(msg)
        return values


class CreateSessionResponse(Schema):
    session: _Session
    class _Session(Schema):  # noqa: E301
        id: UuidField = Field(..., example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")  # noqa: A003
        account_id: IdField = Field(..., example=42)

    tokens: _Tokens
    class _Tokens(Schema):  # noqa: E301
        access_token: str = Field(..., example=(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6N"
            "DJ9.YKVpm2zdxup0_ts81Ft4USo-AUMKXBCTfgXtNFbRLlg"
        ))
        refresh_token: str = Field(..., example=(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MiwiZGV2aWNlX2lkIj"
            "oxOCwiZXhwIjoxNjg3MjU2MTMxfQ.GgXVGPV1aE2GjyRWN_IrHaEkZwY_x0gs25lJKtgspX0"
        ))


class RefreshTokensResponse(Schema):
    access_token: str = Field(..., example=(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6N"
        "DJ9.YKVpm2zdxup0_ts81Ft4USo-AUMKXBCTfgXtNFbRLlg"
    ))
    refresh_token: str = Field(..., example=(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MiwiZGV2aWNlX2lkIj"
        "oxOCwiZXhwIjoxNjg3MjU2MTMxfQ.GgXVGPV1aE2GjyRWN_IrHaEkZwY_x0gs25lJKtgspX0"
    ))
