"""Customized dirty_equals classes useful for testing.

Most of them have rigid structure suitable for our application only.
Since they serve only for testing convenience we didn't want
to make them flexible and extensible. We just "hard-coded" all
things we wanted them to check in tests for our application.
"""

from __future__ import annotations

from datetime import timezone
from typing import TYPE_CHECKING

import dirty_equals

from src.shared.datetime import DATETIME_FORMAT


if TYPE_CHECKING:
    from datetime import datetime
    from typing import Any, Self


class PositiveInt(dirty_equals.IsPositiveInt):
    """Customized dirty_equals.IsPositive."""

    def __init__(self: Self, *, like: int | None = None) -> None:
        """Initialize object.

        :param like: example value (required)

        :raises AssertionError: `like` value is not correct
        """
        assert like is not None, "Provide correct example value in `like` argument."

        self._like = like
        super().__init__()

        try:
            like_equals = self.equals(self._like)

        except TypeError:
            msg = f"`like` argument has type {type(self._like)}, but expected {self.allowed_types}."
            raise AssertionError(msg) from None

        assert like_equals, "Example value from `like` argument is not correct."


class UtcDatetime(dirty_equals.IsDatetime):
    """Customized dirty_equals.IsDatetime to change timezone-aware datetime objects with UTC timezone."""

    def __init__(self: Self, *, like: datetime | None = None) -> None:
        """Initialize object.

        :param like: example value (required)

        :raises AssertionError: `like` value is not correct
        """
        assert like is not None, "Provide correct example value in `like` argument."

        self._like = like
        super().__init__(iso_string=False)

        try:
            like_equals = self.equals(self._like)

        except TypeError:
            msg = f"`like` argument has type {type(self._like)}, but expected {self.allowed_types}."
            raise AssertionError(msg) from None

        assert like_equals, "Example value from `like` argument is not correct."

    def equals(self: Self, other: Any) -> bool:  # noqa: ANN401
        """Return True if `self` "dirty equals" to `other` or False otherwise."""
        return super().equals(other) and other.tzinfo == timezone.utc


class UtcDatetimeStr(dirty_equals.IsDatetime):
    """Customized dirty_equals.IsDatetime to check timezone-aware ISO formatted datetime strings with UTC timezone."""

    expected_format = DATETIME_FORMAT

    def __init__(self: Self, *, like: str | None = None) -> None:
        """Initialize object.

        :param like: example value (required)

        :raises AssertionError: `like` value is not correct
        """
        assert like is not None, "Provide correct example value in `like` argument."

        self._like = like
        super().__init__(format_string=self.expected_format)

        try:
            like_equals = self.equals(self._like)

        except TypeError:
            msg = f"`like` argument has type {type(self._like)}, but expected {self.allowed_types}."
            raise AssertionError(msg) from None

        except ValueError:
            msg = f"`like` argument '{self._like}' does not match expected format '{self.expected_format}'."
            raise AssertionError(msg) from None

        assert like_equals, "Example value from `like` argument is not correct."
