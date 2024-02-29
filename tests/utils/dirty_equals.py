from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import wlss.core.exceptions
from dirty_equals import DirtyEquals
from wlss.shared.types import Id, UtcDatetime


if TYPE_CHECKING:
    from typing import Self


class IsId(DirtyEquals[Id]):
    def equals(self: Self, other: str) -> bool:
        return isinstance(other, Id)


class IsIdSerialized(DirtyEquals[int]):
    def equals(self: Self, other: int) -> bool:
        try:
            Id(other)
        except wlss.core.exceptions.ValidationError:
            return False
        return True


class IsUtcDatetime(DirtyEquals[UtcDatetime]):
    def equals(self: Self, other: str) -> bool:
        return isinstance(other, UtcDatetime)


class IsUtcDatetimeSerialized(DirtyEquals[str]):
    def equals(self: Self, other: str) -> bool:
        try:
            UtcDatetime(datetime.fromisoformat(other))
        except wlss.core.exceptions.ValidationError:
            return False
        return True
