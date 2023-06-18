"""Customized enum class."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, TypeVar


if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from typing import Self


T = TypeVar("T")


class Enum(enum.Enum):
    """Customized `Enum` class from standard library."""

    def __iter__(self: Self) -> Iterator[tuple[str, str]]:  # pragma: no cover
        """Get a tuple with member name and member value.

        It allows us to write this:
        ```python
        _, bucket_name = Bucket.ENTITY
        ```
        instead of this:
        ```python
        bucket_name = Bucket.ENTITY.value  # we assign `value` to `name` which looks weird
        ```

        :returns: Iterator which yields a tuple of `enum_member_name` and `enum_member_value`.
        """
        return iter((self.name, self.value))


def types(*required_types: type[T]) -> Callable[[type[enum.Enum]], type[enum.Enum]]:  # pragma: no cover
    """Raise an error if enum member value type doesn't meet the list of types provided.

    This is a decorator for Enum classes. We can use it in this way.

    :param required_types: required types for Enum attribute values
    :returns: decorator for enum class
    """
    def wrapper(enum_cls: type[enum.Enum]) -> type[enum.Enum]:
        for member in enum_cls.__members__.values():
            if not isinstance(member.value, tuple(required_types)):
                msg = f"Enum values must be instances of one of the following types: {required_types}"
                raise TypeError(msg)
        return enum_cls
    return wrapper


# this assignments here only for convenience and consistency
# it will allow us to import something from our custom `enum` module
# instead of python standard library `enum`
unique = enum.unique
