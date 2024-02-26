from __future__ import annotations

from functools import cache

import bcrypt


@cache
def hashpw(password: bytes, salt: bytes | None = None) -> bytes:
    if salt is None:
        salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)
