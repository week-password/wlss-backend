from __future__ import annotations

from wlss.wish.types import WishDescription, WishTitle

from src.shared.columns import StrColumn


# pylint: disable-next=abstract-method,too-many-ancestors
class WishDescriptionColumn(StrColumn):
    cache_ok = True
    type_ = WishDescription


# pylint: disable-next=abstract-method,too-many-ancestors
class WishTitleColumn(StrColumn):
    cache_ok = True
    type_ = WishTitle
