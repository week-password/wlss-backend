from __future__ import annotations

from src.account.fields import AccountEmailField, AccountLoginField, AccountPasswordField
from src.shared.schemas import Schema


class NewAccount(Schema):
    """Account data which is going to be created during sign up process."""

    email: AccountEmailField
    login: AccountLoginField
    password: AccountPasswordField
