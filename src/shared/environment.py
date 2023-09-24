"""Utilities for working with environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from src import PROJECT_ROOT


if TYPE_CHECKING:
    from typing import Final


def get_dotenv_path() -> Path:  # pragma: no cover
    """Get path to dotenv file resolved from $WLSS_ENV environment variable.

    The value of $WLSS_ENV variable should be one of those (listed in resolution order):

        - path to a directory containing `.env` file relative to `PROJECT_ROOT/envs/`
          example: "local/dev"

        - path to a particular dotenv file relative to `PROJECT_ROOT/envs/`
          example: "local/dev/.my-env"

        - path to a directory containing `.env` file relative to `PROJECT_ROOT/`
          example: "envs/local/dev"

        - path to a dotenv file relative to `PROJECT_ROOT/`
          example: "envs/local/dev/.my-env"

        - absolute path to directory containing `.env` file
          example: "/home/john/"

        - absolute path to directory containing `.env` file
          example: "/home/john/"

        - absolute path to particular dotenv file
          example: "/home/john/.my-env"

    :returns: path to dotenv file

    :raises AssertionError: raised if $WLSS_ENV is not provided
    :raises FileNotFoundError: raised if dotenv file not found
    """
    assert "WLSS_ENV" in os.environ, "Can not load environment variables. Please define $WLSS_ENV environment variable."
    WLSS_ENV: Final = os.environ["WLSS_ENV"]  # noqa: N806

    paths_to_resolve = (
        PROJECT_ROOT / "envs" / WLSS_ENV / ".env",
        PROJECT_ROOT / "envs" / WLSS_ENV,
        PROJECT_ROOT / WLSS_ENV / ".env",
        PROJECT_ROOT / WLSS_ENV,
        Path(WLSS_ENV) / ".env",
        Path(WLSS_ENV),
    )
    for path in paths_to_resolve:
        if path.is_file():
            return path

    raise FileNotFoundError(
        "Cannot find dotenv file resolved from $WLSS_ENV variable.\n"
        "Tried following paths:\n"
        + "\n".join(str(path) for path in paths_to_resolve),
    )
