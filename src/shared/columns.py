from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import types
from wlss.core.types import PositiveInt, Str, Type
from wlss.shared.types import Id, UtcDatetime


if TYPE_CHECKING:
    from typing import Any, Self

    from sqlalchemy.engine.interfaces import Dialect


T = TypeVar("T")


# pylint: disable-next=abstract-method,too-many-ancestors
class TypeColumn(types.TypeDecorator[Type[T]]):
    type_: type[Type[T]]

    def process_bind_param(self: Self, value: Any | None, _: Dialect) -> T | None:  # noqa: SC200
        if isinstance(value, self.type_):
            return value.value
        if value is None:
            return None
        raise NotImplementedError  # pragma: no cover

    def process_result_value(self: Self, value: T | None, _: Dialect) -> Type[T] | None:
        if value is None:
            return None
        return self.type_(value)


# pylint: disable-next=abstract-method,too-many-ancestors
class PositiveIntColumn(TypeColumn[int]):  # pylint: disable=too-many-ancestors
    type_ = PositiveInt
    impl = types.Integer()  # noqa: SC200


# pylint: disable-next=abstract-method,too-many-ancestors
class IdColumn(PositiveIntColumn):  # pylint: disable=too-many-ancestors
    type_ = Id


# pylint: disable-next=abstract-method,too-many-ancestors
class StrColumn(TypeColumn[str]):  # pylint: disable=too-many-ancestors
    type_ = Str
    impl = types.String(length=type_.LENGTH_MAX.value if type_.LENGTH_MAX is not None else None)  # noqa: SC200


# pylint: disable-next=abstract-method,too-many-ancestors
class UtcDatetimeColumn(TypeColumn[datetime]):  # pylint: disable=too-many-ancestors
    type_ = UtcDatetime
    impl = types.DateTime(timezone=True)  # noqa: SC200
