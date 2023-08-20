"""Things used to mock models related functionality."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.shared.database import Base


def __eq__(self: Base, other: Base) -> bool:  # noqa: N807
    """Mock for sqlalchemy models equality check. This function will compare models by equality of object attributes.

    This might be useful in assertion block of our tests to compare model from db to "non-committed" model.
    For example:
    ```python
    users = session.query(User).all()

    # by mocking __eq__ on base model we are able to do this comparison
    assert users == [User(id=42, name="John Doe")]
    ```

    Without using this __eq__ mock we wouldn't be able to compare committed and not committed models
    because sqlalchemy models contain some additional attributes and they have different values
    for these models even if column attributes contain values exactly equal to each other.
    """  # noqa: DAR101, DAR201, RST214, RST215
    for attr in self.__dict__:
        if attr.startswith("_"):
            continue  # skip internal attributes used by sqlalchemy
        if getattr(self, attr) != getattr(other, attr):
            return False
    return True
