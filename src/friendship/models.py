from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, delete, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.friendship.enums import FriendshipRequestStatus
from src.friendship.exceptions import CannotRejectFriendshipRequest
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.friendship.schemas import NewFriendshipRequest


class Friendship(Base):  # pylint: disable=too-few-public-methods

    __tablename__ = "friendship"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False, primary_key=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )


class FriendshipRequest(Base):

    __tablename__ = "friendship_request"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    status: Mapped[FriendshipRequestStatus] = mapped_column(
        Enum(FriendshipRequestStatus, name="friendship_request_status_enum"),
        default=FriendshipRequestStatus.PENDING,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    @classmethod
    async def create(
        cls: type[FriendshipRequest],
        session: AsyncSession,
        new_friendship_request: NewFriendshipRequest,
    ) -> FriendshipRequest:
        friendship_request = FriendshipRequest(
            receiver_id=new_friendship_request.receiver_id,
            sender_id=new_friendship_request.sender_id,
        )
        session.add(friendship_request)
        await session.flush()
        return friendship_request

    async def delete(self: Self, session: AsyncSession) -> None:
        query = delete(FriendshipRequest).where(FriendshipRequest.id == self.id)
        await session.execute(query)
        await session.flush()

    async def accept(self: Self, session: AsyncSession) -> list[Friendship]:
        self.status = FriendshipRequestStatus.ACCEPTED
        friendships = [
            Friendship(account_id=self.sender_id, friend_id=self.receiver_id),
            Friendship(account_id=self.receiver_id, friend_id=self.sender_id),
        ]
        session.add_all(friendships)
        await session.flush()
        return friendships

    async def reject(self: Self, session: AsyncSession) -> None:
        if self.status is not FriendshipRequestStatus.PENDING:
            raise CannotRejectFriendshipRequest()
        self.status = FriendshipRequestStatus.REJECTED
        await session.flush()
