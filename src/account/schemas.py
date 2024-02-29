from __future__ import annotations

from src.account.fields import AccountEmailField, AccountLoginField, AccountPasswordField
from src.profile.schemas import NewProfile, Profile
from src.shared.fields import IdField, UtcDatetimeField
from src.shared.schemas import Schema


class NewAccount(Schema):
    """Account data which is going to be created during sign up process."""

    email: AccountEmailField
    login: AccountLoginField
    password: AccountPasswordField


class Account(Schema):
    id: IdField  # noqa: A003

    created_at: UtcDatetimeField
    email: AccountEmailField
    login: AccountLoginField


class NewAccountWithProfile(Schema):
    account: NewAccount
    profile: NewProfile


class AccountWithProfile(Schema):
    account: Account
    profile: Profile


class AccountId(Schema):
    id: IdField  # noqa: A003


class AccountLogin(Schema):
    login: AccountLoginField


class AccountEmail(Schema):
    email: AccountEmailField
