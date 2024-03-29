from __future__ import annotations

from wlss.profile.types import ProfileDescription, ProfileName

from src.shared.columns import StrColumn


# pylint: disable-next=abstract-method,too-many-ancestors
class ProfileDescriptionColumn(StrColumn):
    cache_ok = True
    type_ = ProfileDescription


# pylint: disable-next=abstract-method,too-many-ancestors
class ProfileNameColumn(StrColumn):
    cache_ok = True
    type_ = ProfileName
