from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from sqlalchemy import and_, CheckConstraint, delete, Enum, ForeignKey, or_, select, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from wlss.shared.types import Id, UtcDatetime

from api.friendship.enums import FriendshipRequestStatus
from src.friendship.exceptions import FriendshipRequestNotFoundError
from src.shared.columns import IdColumn, UtcDatetimeColumn
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.friendship.schemas import NewFriendshipRequest


class Friendship(Base):  # pylint: disable=too-few-public-methods

    __tablename__ = "friendship"

    account_id: Mapped[Id] = mapped_column(ForeignKey("account.id"), nullable=False, primary_key=True)
    friend_id: Mapped[Id] = mapped_column(ForeignKey("account.id"), nullable=False, primary_key=True)

    created_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False)
    updated_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False, onupdate=utcnow)

    __table_args__ = (
        CheckConstraint("account_id != friend_id", name="account_id__friend_id__differ"),
    )


class FriendshipRequest(Base):

    __tablename__ = "friendship_request"

    id: Mapped[Id] = mapped_column(IdColumn, primary_key=True)  # noqa: A003

    created_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False)
    receiver_id: Mapped[Id] = mapped_column(ForeignKey("account.id"), nullable=False)
    sender_id: Mapped[Id] = mapped_column(ForeignKey("account.id"), nullable=False)
    status: Mapped[FriendshipRequestStatus] = mapped_column(
        Enum(FriendshipRequestStatus, name="friendship_request_status_enum"),
        default=FriendshipRequestStatus.PENDING,
        nullable=False,
    )
    updated_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False, onupdate=utcnow)

    __table_args__ = (
        CheckConstraint("sender_id != receiver_id", name="sender_id__receiver_id__differ"),
        UniqueConstraint("sender_id", "receiver_id", name="sender_id__receiver_id__unique_together"),
    )

    @classmethod
    async def create(
        cls: type[FriendshipRequest],
        session: AsyncSession,
        new_friendship_request: NewFriendshipRequest,
    ) -> FriendshipRequest:
        query = delete(FriendshipRequest).where(
            FriendshipRequest.receiver_id == new_friendship_request.receiver_id,
            FriendshipRequest.sender_id == new_friendship_request.sender_id,
        )
        await session.execute(query)
        await session.flush()

        friendship_request = FriendshipRequest(
            receiver_id=new_friendship_request.receiver_id,
            sender_id=new_friendship_request.sender_id,
        )
        session.add(friendship_request)
        await session.flush()
        return friendship_request

    @classmethod
    async def get(
        cls: type[FriendshipRequest],
        session: AsyncSession,
        request_id: Id,
    ) -> FriendshipRequest:
        query = select(FriendshipRequest).where(FriendshipRequest.id == request_id)
        row = (await session.execute(query)).one_or_none()
        if row is None:
            raise FriendshipRequestNotFoundError()
        return typing.cast(FriendshipRequest, row.FriendshipRequest)

    async def delete(self: Self, session: AsyncSession) -> None:
        query = delete(FriendshipRequest).where(FriendshipRequest.id == self.id)
        await session.execute(query)
        await session.flush()

    async def accept(self: Self, session: AsyncSession) -> list[Friendship]:
        friendships = [
            Friendship(account_id=self.sender_id, friend_id=self.receiver_id),
            Friendship(account_id=self.receiver_id, friend_id=self.sender_id),
        ]
        session.add_all(friendships)
        await session.flush()

        query = (
            delete(FriendshipRequest)
            .where(
                or_(
                    and_(
                        FriendshipRequest.sender_id == self.sender_id,
                        FriendshipRequest.receiver_id == self.receiver_id,
                    ),
                    and_(
                        FriendshipRequest.sender_id == self.receiver_id,
                        FriendshipRequest.receiver_id == self.sender_id,
                    ),
                ),
            )
        )
        await session.execute(query)
        return friendships

    async def reject(self: Self, session: AsyncSession) -> None:
        self.status = FriendshipRequestStatus.REJECTED
        await session.flush()
