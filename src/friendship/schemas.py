from __future__ import annotations

from src.shared.fields import IdField
from src.shared.schemas import Schema


class NewFriendshipRequest(Schema):
    receiver_id: IdField
    sender_id: IdField
