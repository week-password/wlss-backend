from __future__ import annotations

from wlss.account.types import AccountEmail, AccountLogin

from src.shared.columns import StrColumn


# pylint: disable-next=abstract-method,too-many-ancestors
class AccountEmailColumn(StrColumn):
    cache_ok = True
    type_ = AccountEmail


# pylint: disable-next=abstract-method,too-many-ancestors
class AccountLoginColumn(StrColumn):
    cache_ok = True
    type_ = AccountLogin
