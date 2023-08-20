"""Field definitions shared by different application components."""

from __future__ import annotations

import re
from typing import final, TYPE_CHECKING

from overrides import override
from pydantic import SecretStr


if TYPE_CHECKING:
    from collections.abc import Callable, Generator
    from typing import Any

    from pydantic import PositiveInt


class StrField(str):
    """String field for Pydantic models."""

    FIELD_NAME: str = "Value"
    LENGTH_MAX: PositiveInt
    LENGTH_MIN: PositiveInt
    REGEXP: str | None = None

    @classmethod
    def __get_validators__(
        cls: type[StrField],
    ) -> Generator[Callable[[str], str | StrField], None, None]:
        """Pydantic's special method. Can be overridden in sub-classes."""
        yield cls._validate_length
        yield cls._validate_regexp
        yield cls.cast_type

    def __init_subclass__(cls: type[StrField]) -> None:  # pragma: no cover
        """Validate subclass for the presence of required class attributes and other constraints."""
        if not hasattr(cls, "LENGTH_MIN") or not hasattr(cls, "LENGTH_MAX"):
            msg = "LENGTH_MIN or LENGTH_MAX should be defined in a subclass."
            raise RuntimeError(msg)
        if cls.LENGTH_MIN > cls.LENGTH_MAX:
            msg = "LENGTH_MIN cannot be greater than LENGTH_MAX"
            raise RuntimeError(msg)

    @classmethod
    @final
    def _validate_length(cls: type[StrField], value: str) -> str:  # pragma: no cover
        if len(value) < cls.LENGTH_MIN:
            msg = f"{cls.FIELD_NAME} length should not be less than {cls.LENGTH_MIN}."
            raise ValueError(msg)
        if len(value) > cls.LENGTH_MAX:
            msg = f"{cls.FIELD_NAME} length should not be greater than {cls.LENGTH_MAX}."
            raise ValueError(msg)
        return value

    @classmethod
    @final
    def _validate_regexp(cls: type[StrField], value: str) -> str:  # pragma: no cover
        if cls.REGEXP is not None and not re.fullmatch(cls.REGEXP, value):
            msg = rf"{cls.FIELD_NAME} should match regular expression: {cls.REGEXP}"
            raise ValueError(msg)
        return value

    @classmethod
    def cast_type(cls: type[StrField], value: str) -> StrField:  # pragma: no cover
        """Cast value type to the corresponding class after all validations are completed.

        Can be overridden in sub-classes.

        :param value: string value after all validations
        :return: instance of the class which string value have been cast to
        """
        return cls(value)

    @classmethod
    def __modify_schema__(cls: type[StrField], field_schema: dict[str, Any]) -> None:  # pragma: no cover
        """Pydantic's special method to modify field representation in OpenAPI schema."""
        field_schema.update({
            "length_max": cls.LENGTH_MAX,
            "length_min": cls.LENGTH_MIN,
            "regexp": cls.REGEXP,
        })


class SecretStrField(SecretStr):
    """String field which value should be secret and not exposed in logging accidentally.

    We duplicated all StrField functionality here instead of using multiple inheritance in order to avoid
    method resolution order issues which may come with multiple inheritance.
    """

    FIELD_NAME: str = "Value"
    LENGTH_MAX: PositiveInt
    LENGTH_MIN: PositiveInt
    REGEXP: str | None = None

    def __init_subclass__(cls: type[SecretStrField]) -> None:  # pragma: no cover
        """Validate subclass for the presence of required class attributes and other constraints."""
        if not hasattr(cls, "LENGTH_MIN") or not hasattr(cls, "LENGTH_MAX"):
            msg = "LENGTH_MIN or LENGTH_MAX should be defined in a subclass."
            raise RuntimeError(msg)
        if cls.LENGTH_MIN > cls.LENGTH_MAX:
            msg = "LENGTH_MIN cannot be greater than LENGTH_MAX"
            raise RuntimeError(msg)

    @classmethod
    @override
    def __get_validators__(
        cls: type[SecretStrField],
    ) -> Generator[Callable[[str], str | SecretStrField], None, None]:  # pragma: no cover
        """Pydantic's special method. Can be overridden in sub-classes."""
        yield cls._validate_length
        yield cls._validate_regexp
        yield cls.cast_type

    @classmethod
    @final
    def _validate_length(cls: type[SecretStrField], value: str) -> str:  # pragma: no cover
        if len(value) < cls.LENGTH_MIN:
            msg = f"{cls.FIELD_NAME} length should not be less than {cls.LENGTH_MIN}."
            raise ValueError(msg)
        if len(value) > cls.LENGTH_MAX:
            msg = f"{cls.FIELD_NAME} length should not be greater than {cls.LENGTH_MAX}."
            raise ValueError(msg)
        return value

    @classmethod
    @final
    def _validate_regexp(cls: type[SecretStrField], value: str) -> str:  # pragma: no cover
        if cls.REGEXP is not None and not re.fullmatch(cls.REGEXP, value):
            msg = rf"{cls.FIELD_NAME} should match regular expression: {cls.REGEXP}"
            raise ValueError(msg)
        return value

    @classmethod
    def cast_type(cls: type[SecretStrField], value: str) -> SecretStrField:  # pragma: no cover
        """Cast value type to the corresponding class after all validations are completed.

        Can be overridden in sub-classes.

        :param value: string value after all validations
        :return: instance of the class which string value have been cast to
        """
        return cls(value)

    @classmethod
    @override
    def __modify_schema__(cls: type[SecretStrField], field_schema: dict[str, Any]) -> None:  # pragma: no cover
        """Pydantic's special method to modify field representation in OpenAPI schema."""
        field_schema.update({
            "length_max": cls.LENGTH_MAX,
            "length_min": cls.LENGTH_MIN,
            "regexp": cls.REGEXP,
        })
