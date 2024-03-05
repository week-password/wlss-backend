from __future__ import annotations

from src.shared.enum import Enum, types


@types(str)
class FriendshipRequestStatus(Enum):
    PENDING = "PENDING"
    REJECTED = "REJECTED"
