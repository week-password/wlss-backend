from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from redis.asyncio import Redis

from src.auth.exceptions import SessionNotFoundError
from src.auth.schemas import SessionData
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self
    from uuid import UUID

    from wlss.shared.types import Id


class SessionStorage:
    def __init__(self: Self, host: str, port: str) -> None:
        self._redis = Redis(host=host, port=int(port), decode_responses=True)

    async def create_session(self: Self, account_id: Id) -> SessionData:
        session_data = SessionData(
            account_id=account_id,
            created_at=utcnow(),
            id=uuid.uuid4(),
        )
        await self._redis.hset(
            f"account_id:{account_id.value}",
            str(session_data.id),
            session_data.model_dump_json(),
        )
        return session_data

    async def get_session(self: Self, account_id: Id, session_id: UUID) -> SessionData:
        response = await self._redis.hget(f"account_id:{account_id.value}", str(session_id))
        if response is None:
            raise SessionNotFoundError()
        return SessionData.model_validate_json(response)

    async def has_session(self: Self, account_id: Id, session_id: UUID) -> bool:
        return await self._redis.hexists(f"account_id:{account_id.value}", str(session_id))

    async def delete_session(self: Self, account_id: Id, session_id: UUID) -> None:
        await self._redis.hdel(f"account_id:{account_id.value}", str(session_id))

    async def delete_all_sessions(self: Self, account_id: Id) -> None:
        await self._redis.delete(f"account_id:{account_id.value}")
