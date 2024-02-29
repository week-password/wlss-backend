from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from wlss.shared.types import UtcDatetime


if TYPE_CHECKING:
    from typing import Final


DATETIME_FORMAT: Final = "%Y-%m-%dT%H:%M:%S.%fZ"


def utcnow() -> UtcDatetime:
    """Get timezone aware datetime with UTC timezone.

    There are two reasons of having this function instead of just using `datetime.now(tz=timezone.utc)` everywhere:

        1. We have to provide a callable to sqlalchemy column definition which should return timezone-aware datetime.

           It means that we can not provide just `default=datetime.now` because it is not using UTC timezone.
           We also can not use `default=datetime.utcnow` because it returns timezone-naive datetime object.

        2. Simply `utcnow()` is shorter than `UtcDatetime(datetime.now(tz=timezone.utc))`

    :returns: datetime
    """
    return UtcDatetime(datetime.now(tz=timezone.utc))
