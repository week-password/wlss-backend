"""Constants related to file."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Final


BYTE: Final = 1
KILOBYTE: Final = 1024 * BYTE
MEGABYTE: Final = 1024 * KILOBYTE
