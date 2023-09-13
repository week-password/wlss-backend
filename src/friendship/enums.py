"""Enumerations for friendship functionality."""

from __future__ import annotations

from src.shared.enum import Enum, types


@types(str)
class FriendshipRequestStatus(Enum):
    """Possible friendship request statuses."""

    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
