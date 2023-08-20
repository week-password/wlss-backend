"""Utilities for working with date and time."""

from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Get timezone aware datetime with UTC timezone.

    There are two reasons of having this function instead of just using `datetime.now(tz=timezone.utc)` everywhere:

        1. We're using `freezgun` library which cannot mock datetime in sqlalchemy's column definitions, like:
        ```python
        created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
        ```
        because class level attributes are evaluated at compile time. This happens before `freezegun`
        has patched datetime.datetime.now, so the column default functions still point to the stdlib implementation.
        See this SO answer for details: https://stackoverflow.com/a/58776798/8431075

        That's why we should wrap datetime.utcnow to another function.

        2. Simply `utcnow()` is shorter than `datetime.now(tz=timezone.utc)`

    :returns: datetime
    """
    return datetime.now(tz=timezone.utc)
