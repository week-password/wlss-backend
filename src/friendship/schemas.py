from __future__ import annotations

from api.shared.fields import IdField
from api.shared.schemas import Schema


class NewFriendshipRequest(Schema):
    receiver_id: IdField
    sender_id: IdField
