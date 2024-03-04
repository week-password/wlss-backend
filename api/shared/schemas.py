from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class Schema(BaseModel):
    """Customized 'BaseModel' class from pydantic."""

    @classmethod
    def from_(cls: type[T], model: Schema) -> T:
        return cls.model_validate(model.model_dump())
